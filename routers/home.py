from config.database import SessionLocal
from fastapi import APIRouter
from models.models import Product

router = APIRouter(
    tags = ["Home Page"]
)

session = SessionLocal()

@router.post("/discount")
async def highly_discounted():
    products = session.query(Product).filter(Product.discount >=0.4).all()
    for product in products:
        return product
    
@router.post("/top_sellers")
async def top_sellers():
    pass
