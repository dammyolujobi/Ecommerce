from fastapi import APIRouter,Response,Request
from schemas.schema import CartBase,SalesBase
from routers.users import get_current_user
from routers.sessions import get_or_create_session_id
from config.database import SessionLocal
from models.models import UserCarts,GuestCarts,Sales
from datetime import datetime, timedelta,timezone
router = APIRouter(
    prefix="/user"
)

#Initialize session
session = SessionLocal()


@router.post("users/product")
def add_to_cart(cart:CartBase,request:Request,response:Response):
    customer_id = get_current_user()
    session_id = get_or_create_session_id(request,response)
    if not cart.customer_id:
        expires_at = datetime.now(timezone.utc) + timedelta(days=7)
        add_guest_cart = GuestCarts(
                product_id = cart.product_id,
                session_id = session_id,
                quantity = cart.quantity,
                expires_at = expires_at
        )

        session.add(add_guest_cart)
        session.commit()
        session.refresh(add_guest_cart)

    elif cart.customer_id:
        add_cutomer_cart = UserCarts(
            customer_id = customer_id,
            product_id = cart.product_id,
            quantity = cart.quantity,
            expires_at = expires_at
        )
        
        session.add(add_cutomer_cart)
        session.commit()
        session.refresh(add_cutomer_cart)

        

@router.post("/sales")
async def sales_detail(sales:SalesBase):
    
    add_sales_detail = Sales(**sales.model_dump())
    session.add(add_sales_detail)
    session.commit()
    session.refresh(add_sales_detail)

