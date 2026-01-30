from config.database import SessionLocal
from fastapi import APIRouter
from models.models import Product

router = APIRouter(
    tags = ["Home Page"]
)

session = SessionLocal()

@router.get("/discount")
async def highly_discounted():
    products = session.query(Product).filter(Product.discount > 0.4).all()
    return products
    
@router.post("/top_sellers")
async def top_sellers():
    init_store = []
    fin_store = []
    products = session.query(Product).all()
    
    for product in products:
        if product.discount > 0:
            init_store.append(product)

    for _ in init_store:
        fin_store.append(max(init_store))
        init_store.remove(max(init_store))

    return fin_store