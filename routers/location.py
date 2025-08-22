from fastapi import APIRouter,Request

router = APIRouter(
    tags=["location"]
)

#Unfinished for getting the country part
@router.get("/get_country")
def get_country(request:Request)->str:
    forwarded = request.headers.get("x-forwarded-for")
    
    if forwarded:
        ip_address = forwarded
    else:
        ip_address = request.client.host

    country = request.get(f"http://ip-api.com/json/{ip_address}")

    return country




