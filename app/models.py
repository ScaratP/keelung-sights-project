from pydantic import BaseModel

class Sight(BaseModel):
    sight_name: str
    zone: str
    category: str
    photo_url: str
    description: str
    address: str
