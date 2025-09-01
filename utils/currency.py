from fastapi import APIRouter
import requests
import os
from dotenv import load_dotenv
import json

load_dotenv()

CURRENCY_API_KEY = os.getenv("CURRENCY_API_KEY")

router = APIRouter(
    tags=["location"]
)

LOCATION_API_KEY = os.getenv("LOCATION_API_KEY")

def get_country():
    #Store the information gotten from the requests urls
    ip_store = {}
    country_info = {}

    #Get the current ip address
    request = requests.get("http://ipinfo.io/json")
    ip_store.update(request.json())
    ip_address = ip_store["ip"]

    #Get the location info 
    country = requests.get(f"https://api.ipinfo.io/lite/{ip_address}?token={LOCATION_API_KEY}")
    country_info.update(country.json())

    return country_info["country"]

def get_country_currency()->str:
    data = {}

    with open("routers/country_list.json","r") as f:
        data.update(json.load(f))

    current_country = get_country()

    for country in data["countries"]:
        if current_country.lower() != country["country"].lower():
            pass
        else:
            return country["currency"]
                
def get_exchange_rate(against_curr:str):
    exchange_rate = {}

    response = requests.get(f"https://v6.exchangerate-api.com/v6/{CURRENCY_API_KEY}/latest/{get_country_currency()}")
    exchange_rate.update(response.json())   

    result = exchange_rate["conversion_rates"].get(against_curr)
    return result
