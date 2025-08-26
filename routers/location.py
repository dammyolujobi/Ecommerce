from fastapi import APIRouter,Request
import requests

router = APIRouter(
    tags=["location"]
)

#Unfinished for getting the country part

def get_country():
    country = {}
    request = requests.get("http://ipinfo.io/json")
    country.update(request.json())
    return country["country"]

country = requests.get("http://ipinfo.io/json")
print(country.json())


