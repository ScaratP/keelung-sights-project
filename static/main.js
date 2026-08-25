document.addEventListener('DOMContentLoaded', () => {
    const buttons = document.querySelectorAll('.custom-zone-btn');
    const container = document.getElementById('sights-container');
    const loading = document.getElementById('loading');

    buttons.forEach(button => {
        button.addEventListener('click', (e) => {
            buttons.forEach(b => b.classList.remove('active'));
            e.target.classList.add('active');
            const zone = button.getAttribute('data-zone');
            fetchSights(zone);
        });
    });

    async function fetchSights(zone) {
        container.innerHTML = '';
        loading.classList.remove('d-none');
        
        try {
            const response = await fetch(`/sights?zone=${zone}`);
            
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            
            const data = await response.json();
            
            if (data.length === 0) {
                container.innerHTML = `
                    <div class="col-12 text-center text-muted my-5">
                        <p class="mb-2">該區域目前無景點資料</p>
                        <small>請管理員執行 <code>python -m app.seed_data</code> 更新資料庫</small>
                    </div>`;
                return;
            }
            
            data.forEach((sight) => {
                const col = document.createElement('div');
                col.className = 'col-12 col-md-4 d-flex align-items-stretch';
                
                const mapUrl = `https://www.google.com/maps/search/?api=1&query=${encodeURIComponent(sight.address)}`;
                
                const isLongText = sight.description.length > 60;
                const showMoreBtn = isLongText ? `<button class="show-more-btn" onclick="toggleText(this)">顯示更多</button>` : '';
                
                // 處理無圖片或圖片失效的顯示邏輯
                const fallbackHTML = `<div class="no-image-placeholder">該景點沒有提供圖片</div>`;
                let imageContent = fallbackHTML;
                
                // 確認有網址，且不是當初爬蟲防呆用的 placeholder 假圖
                if (sight.photo_url && sight.photo_url.startsWith('http') && !sight.photo_url.includes('via.placeholder.com')) {
                    // 若圖片載入失敗 (onerror)，則將 img 標籤替換為 fallbackHTML 佔位區塊
                    const safeFallback = fallbackHTML.replace(/"/g, '&quot;');
                    imageContent = `<img src="${sight.photo_url}" class="card-img-custom" alt="${sight.sight_name}" onerror='this.outerHTML="${safeFallback}"'>`;
                }
                
                col.innerHTML = `
                    <div class="custom-card w-100">
                        ${imageContent}
                        
                        <div class="card-body d-flex flex-column p-4">
                            <h5 class="mb-3" style="font-weight: 500;">${sight.sight_name}</h5>
                            
                            <div class="mb-3">
                                <span class="custom-badge me-1">${sight.zone}</span> 
                                <span class="custom-badge category">${sight.category}</span>
                            </div>
                            
                            <div class="desc-container mb-3">
                                <p class="sight-desc mb-0">${sight.description}</p>
                                ${showMoreBtn}
                            </div>

                            <div class="card-footer-custom">
                                <span class="address-text">${sight.address}</span>
                                <a href="${mapUrl}" target="_blank" class="map-link">Google Maps</a>
                            </div>
                        </div>
                    </div>
                `;
                container.appendChild(col);
            });
        } catch (error) {
            console.error('Error fetching sights:', error);
            container.innerHTML = `
                <div class="col-12 text-center my-5" style="color: #7B8B88;">
                    <p>發生錯誤，請確認 API 伺服器狀態</p>
                </div>`;
        } finally {
            loading.classList.add('d-none');
        }
    }

    // 將切換文字的函式掛載到 window，讓行內的 onclick 可以呼叫
    window.toggleText = function(btn) {
        const desc = btn.previousElementSibling;
        if (desc.classList.contains('expanded')) {
            desc.classList.remove('expanded');
            btn.textContent = '顯示更多';
        } else {
            desc.classList.add('expanded');
            btn.textContent = '收起內容';
        }
    };
});