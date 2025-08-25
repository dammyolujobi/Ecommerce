from fastapi import APIRouter,Response,Request,Depends
from schemas.schema import CartBase,SalesBase
from routers.users import get_current_user
from routers.sessions import get_or_create_session_id
from config.database import SessionLocal
from models.models import UserCarts,GuestCarts,Sales,Customer
from datetime import datetime, timedelta,timezone
router = APIRouter(
    prefix="/user",
    tags=["sales"]
)

#Initialize session
session = SessionLocal()

session_id = get_or_create_session_id(Request,Response)

@router.post("/users/product")
def add_to_cart(
                quantity,
                product_id,
                user_name:str = Depends(get_current_user)
                ):

    #Get all user details
    user = session.query(Customer).filter(Customer.first_name == user_name).first()

    customer_id = user.id
    
    if not user_name:
        expires_at_time = datetime.now(timezone.utc) + timedelta(days=7)
        add_guest_cart = GuestCarts(
                product_id = product_id,
                session_id = session_id,
                quantity = quantity,
                expires_at = expires_at_time
        )

        session.add(add_guest_cart)
        session.commit()
        session.refresh(add_guest_cart)

    elif customer_id:
        add_cutomer_cart = UserCarts(
            customer_id = customer_id,
            product_id = product_id,
            quantity = quantity,

        )
        
        session.add(add_cutomer_cart)
        session.commit()
        session.refresh(add_cutomer_cart)
    
    return add_cutomer_cart

@router.post("/sales")
async def sales_detail(sales:SalesBase = Depends()):

    add_sales_detail = Sales(**sales.model_dump())
    session.add(add_sales_detail)
    session.commit()
    session.refresh(add_sales_detail)

    return sales
