from fastapi import APIRouter
from models.models import UserCarts,Product,Customer
from config.database  import SessionLocal
from routers.location import get_country
from routers.payment import initiate_payment,verify_payment
session = SessionLocal()

router = APIRouter(
    tags=["Checkout"]
)


@router.post("/checkout")

def checkout(user_id:str):
    cart_info = session.query(UserCarts).filter(UserCarts.customer_id == user_id).first()
    
    product_id = cart_info.product_id

    product = session.query(Product).filter(Product.id == product_id).first()

    price_of_prod = product.price
    discount = product.discount

    user = session.query(Customer).filter(Customer.id == user_id).first()

    user_email = user.email
    
    disc_price = discount * price_of_prod

    if get_country == None: 
        currency = "NGN"
        initiate_payment(user_email,disc_price,currency)

    else:
        initiate_payment(user_email,disc_price,get_country)

    





