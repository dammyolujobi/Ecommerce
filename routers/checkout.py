from fastapi import APIRouter,Depends
from models.models import UserCarts,Product,Customer
from config.database  import SessionLocal
from routers.payment import initiate_payment
from routers.users import get_current_user
from utils.currency import get_country_currency,get_exchange_rate
import os
import requests
from dotenv import load_dotenv

currency = get_country_currency()
load_dotenv()

PSK_URL = f"https://api.paystack.co/transaction"
PSK_SECRET_KEY = os.getenv("PSK_SECRET_KEY")

session = SessionLocal()

router = APIRouter(
    tags=["checkout"]
)

@router.post("/checkout")
async def checkout(user_name:str = Depends(get_current_user)):

    prod_id_store = []
    price_store = []
    discount_store = []
    discount = 0
    quantity_store = []
    
    user = session.query(Customer).filter(Customer.first_name == user_name).first()

    user_id  = user.id
    
    cart_info = session.query(UserCarts).filter(UserCarts.customer_id == user_id).all()

    # Append product id gotten from cart_info into prod_id_store
    for cart in range(0,len(cart_info)):
        prod_id_store.append(cart_info[cart].product_id)
        quantity_store.append(cart_info[cart].quantity)

    # Append price and discount gotten from prod_id_store
    for product_id in prod_id_store:
 
        product = session.query(Product).filter(Product.id == product_id).all()
            
        for prod in product:
            rate_for_prod = get_exchange_rate(prod.currency)
            price_store.append(prod.price*rate_for_prod)
            discount_store.append(prod.discount)
    

    for i in range(0,len(price_store)):
        discount += discount_store[i] * price_store[i] * quantity_store[i]

    user_email = user.email

    payment = initiate_payment(user_email,discount,currency)

    return payment["reference"]

@router.get("/verify_payment")
async def verify_payment(transaction_id:str = Depends(checkout)):
    verify_info = {}
    url = f"{PSK_URL}/verify/{transaction_id} "

    header = {
        "Authorization": f"Bearer {PSK_SECRET_KEY}"
    }

    response = requests.get(url=url,headers=header)
    
    verify_info.update(response.json())
    
    if verify_info["status"] is True and verify_info["message"] == "Verification successful":
        return {"status":"Payment successful","data":verify_info}
    else:
        return {"status": "Payment failed", "data":verify_info}

    