import os
from dotenv import load_dotenv
from fastapi import APIRouter,HTTPException,Depends
import uuid
import requests

load_dotenv()



PSK_SECRET_KEY = os.getenv("PSK_SECRET_KEY")
FLW_ACCESS_TOKEN = os.getenv("FLW_ACCESS_TOKEN")

PSK_URL = f"https://api.paystack.co/transaction"
router = APIRouter(
    prefix="/payment",
    tags=["payment"]
    )
                  

redirect_url = ""

def initiate_payment(email:str,amount:float,currency:str = "NGN")->str:
    payment_info =  {}
    url = f"{PSK_URL}/initialize"

    header = {
        "Authorization" : f"Bearer {PSK_SECRET_KEY}",
        "Content-Type" : "application/json",
    }

    tr_ref = "tr_ref" + str(uuid.uuid4())

    body = {
        "email":email,
        "currency":currency,
        "reference":str(tr_ref),
        "amount": amount,
    }

    response = requests.post(url=url,headers=header,json=body)
    
    if response.status_code !=200:
        raise HTTPException(status_code=response.status_code,detail="Payment initialization failed")
    else:
        payment_info.update(response.json())
        return payment_info["data"]





