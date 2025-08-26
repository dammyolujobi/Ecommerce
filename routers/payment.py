import os
from dotenv import load_dotenv
from fastapi import APIRouter,HTTPException
import uuid
import requests

load_dotenv()

PSK_URL = "https://api.paystack.co/transaction/sk_test_9e162986751fe226fc9a606f1eec62c6cc387c07"

PSK_SECRET_KEY = os.getenv("PSK_SECRET_KEY")
FLW_ACCESS_TOKEN = os.getenv("FLW_ACCESS_TOKEN")

router = APIRouter(
    prefix="/payment",
    tags=["payment"]
    )
                  

redirect_url = ""

def initiate_payment(email:str,amount:float,currency:str = "NGN"):

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
        raise HTTPException(status_code=response.status_code,detail="Payment initializtion failed")
    else:
        return response.json()

@router.get("/payment/{transaction_id}")
def verify_payment(transaction_id:str):

    url = f"{PSK_URL}/transactions/{transaction_id}/verify_id"

    header = {
        "Authorization": f"Bearer{FLW_ACCESS_TOKEN}"
    }

    response = requests.get(url=url,headers=header)
    
    data = response.json()

    if data["status"] == 'success' and data["data"]["status"] == "successful":
        return {"status":"Payment successful","data":data}
    else:
        return {"status": "Payment failed", "data":data}

