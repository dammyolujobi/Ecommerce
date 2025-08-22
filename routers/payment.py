import os
from dotenv import load_dotenv
from fastapi import APIRouter,HTTPException
import uuid
import requests

load_dotenv()

FLW_BASE_URL = 'https://api.flutterwave.cloud/developersandbox'

#For production "https://api.flutterwave.com/v3"

FLW_ACCESS_TOKEN = os.getenv("FLW_ACCESS_TOKEN")

router = APIRouter(
    prefix="/payment",
    tags=["payment"]
    )
                  

redirect_url = ""

def initiate_payment(email:str,amount:float,currency:str = "NGN"):

    url = f"{FLW_BASE_URL}/payments"

    trans_ref = "txn_" + str(uuid.uuid4())

    header = {
        "Authorization" : f"Bearer{FLW_ACCESS_TOKEN}",
        "Content-Type" : "application/json",
        "X-Idempotency-Key" : trans_ref
    }

    payload = {
        "tx_ref" : "",
        "amount": str(amount),
        "currency": currency,
        "redirect_url" : redirect_url,

        "customer" : {
            "email":email,
        },

        "customiztions": {
            "title":"Payment for products"
        }
    }

    response = requests.post(url=url,headers=header,json=payload)

    if response.status_code !=200:
        raise HTTPException(status_code=response.status_code,detail="Payment initializtion failed")
    
    return response.json

@router.get("/payment/{transaction_id}")
def verify_payment(transaction_id:str):

    url = f"{FLW_BASE_URL}/transactions/{transaction_id}/verify_id"

    header = {
        "Authorization": f"Bearer{FLW_ACCESS_TOKEN}"
    }

    response = requests.get(url=url,headers=header)
    
    data = response.json()

    if data["status"] == 'success' and data["data"]["status"] == "successful":
        return {"status":"Payment successful","data":data}
    else:
        return {"status": "Payment failed", "data":data}

