import requests
from bs4 import BeautifulSoup
import time
import logging
from app.models import Sight

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class KeelungSightsCrawler:
    """
    基隆景點網頁爬蟲
    目標網址：https://okgo.tw/buty/keelung.html
    """
    BASE_URL = "https://okgo.tw/buty/keelung.html"
    DOMAIN = "https://okgo.tw"

    def get_items(self, zone: str) -> list[Sight]:
        sights = []
        try:
            logger.info(f"開始爬取 {zone} 的景點...")
            headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
            res = requests.get(self.BASE_URL, headers=headers, timeout=10)
            res.raise_for_status()
            soup = BeautifulSoup(res.text, 'html.parser')

            # ================= 第一層：尋找區域與景點網址 =================
            # 1. 根據傳入的 zone (例如: 仁愛區)，尋找包含該區名的 <h2> 標籤
            zone_h2 = soup.find('h2', string=lambda t: t and zone in t)
            detail_urls = set()
            
            if zone_h2:
                # 2. 往上找到包含該區所有景點的父容器 <div class="sec2">
                sec_div = zone_h2.find_parent('div', class_='sec2')
                if sec_div:
                    # 3. 抓取該區塊內所有的景點連結 (ul.dot 裡面的 a 標籤)
                    a_tags = sec_div.select("ul.dot li > a")
                    for a in a_tags:
                        href = a.get('href', '')
                        # 4. 確認是詳細頁面的網址
                        if 'butyview.html' in href:
                            # 將 '../butyview.html' 轉為絕對網址 'https://okgo.tw/butyview.html'
                            clean_href = href.replace('../', '/')
                            if not clean_href.startswith('http'):
                                detail_url = self.DOMAIN + clean_href
                            else:
                                detail_url = clean_href
                            detail_urls.add(detail_url)
            else:
                logger.warning(f"在網頁中找不到包含 '{zone}' 的區塊")

            # ================= 第二層：進入詳細頁面抓資料 =================
            count = 0
            for detail_url in detail_urls:
                try:
                    time.sleep(1)  # 禮貌性等待
                    logger.info(f"爬取詳細頁面: {detail_url}")
                    detail_res = requests.get(detail_url, headers=headers, timeout=10)
                    detail_res.raise_for_status()
                    detail_soup = BeautifulSoup(detail_res.text, 'html.parser')
                    
                    # 剖析內容 (根據實際 HTML 結構提取)
                    
                    # 1. 抓取標題 (<h2> 且有特定 style 或直接抓包含在 sec3 內的 h2)
                    sec3_div = detail_soup.find('div', class_='sec3')
                    title_elem = sec3_div.find('h2') if sec3_div else None
                    sight_name = title_elem.text.strip() if title_elem else "未知景點"
                    
                    # 2. 抓取地址
                    address_text = ""
                    if sec3_div:
                        # 將 sec3_div 的文字內容轉為字串並分割，尋找包含「地址：」的那一行
                        text_content = sec3_div.get_text(separator='\n')
                        for line in text_content.split('\n'):
                            if '地址：' in line or '地址:' in line:
                                address_text = line.replace('地址：', '').replace('地址:', '').strip()
                                break
                    if not address_text:
                        address_text = f"基隆市{zone}未知地址"
                        
                    # 3. 抓取圖片
                    pic_div = detail_soup.find('div', id='Buty_Title_Pic')
                    img_elem = pic_div.find('img') if pic_div else None
                    photo_url = img_elem.get('src') if img_elem else "https://via.placeholder.com/400x300?text=No+Image"
                    
                    # 確保圖片網址是絕對路徑
                    if photo_url and not photo_url.startswith('http'):
                        if photo_url.startswith('//'):
                            photo_url = "https:" + photo_url
                        else:
                            photo_url = self.DOMAIN + photo_url
                    
                    # 4. 抓取描述
                    description = ""
                    if sec3_div:
                        # 尋找 sec3 裡面所有的 <p> 或 <div> 標籤，過濾掉短字串，取最長的一段當作描述
                        text_blocks = [elem.text.strip() for elem in sec3_div.find_all(['p', 'div'])]
                        # 過濾掉包含「文章來源」、「全天開放」等非主要描述的雜訊
                        filtered_blocks = [t for t in text_blocks if len(t) > 30 and '文章來源' not in t and 'Facebook' not in t]
                        
                        if filtered_blocks:
                            description = max(filtered_blocks, key=len)
                            
                    # 截斷過長的描述
                    description = description[:200] + "..." if len(description) > 200 else (description or f"這是位於{zone}的著名景點，值得一遊。")
                    
                    category = "風景區" 
                    
                    sights.append(Sight(
                        sight_name=sight_name,
                        zone=zone,
                        category=category,
                        photo_url=photo_url,
                        description=description,
                        address=address_text
                    ))
                    count += 1
                    
                except requests.exceptions.RequestException as e:
                    logger.warning(f"網路連線失敗 {detail_url}: {e}")
                except Exception as e:
                    logger.warning(f"剖析欄位失敗 {detail_url}: {e}")
                    
        except requests.exceptions.RequestException as e:
            logger.error(f"HTTP 狀態碼異常或連線錯誤: {e}")
            
        # ================= 防呆機制 =================
        # 若爬蟲沒有抓到，做為防呆回傳假資料以利作業展示流程
        if not sights:
            logger.info(f"未爬取到資料，建立 {zone} 的示範資料。")
            sights.append(Sight(
                sight_name=f"{zone}示範景點",
                zone=zone,
                category="觀光地標",
                photo_url="https://via.placeholder.com/400x300?text=Demo+Sight",
                description=f"這是 {zone} 的一個美麗景點，由於爬蟲未命中真實資料而自動生成的測試內容。",
                address=f"基隆市{zone}示範路1號"
            ))
            
        return sights