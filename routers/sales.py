from fastapi import APIRouter,Response,Request
from schemas.schema import CartBase
from routers.users import get_current_user
from routers.sessions import get_or_create_session_id
from config.database import conn,cursor
from datetime import datetime, timedelta,timezone
router = APIRouter(
    prefix="/user"
)

@router.post("users/product")
def add_to_cart(cart:CartBase,request:Request,response:Response):
    cart.customer_id = get_current_user()
    session_id = get_or_create_session_id(request,response)
    if not cart.customer_id:
        expires_at = datetime.now(timezone.utc) + timedelta(days=7)
        values = ("""
            INSERT INTO guest_carts(session_id,quantity,product_id,expires_at)
            VALUES(%s,%s,%s,%s,%s)
                """)
        params = (
            session_id,
            cart.quantity,
            cart.product_id,
            expires_at
        )
        cursor.execute(values,params)
        conn.commit()
    elif cart.customer_id:
        values = (
            """
        INSERT INTO user_carts(customer_id,product_id,quantity)
        VALUE(%s,%s,%s)
            """
        )
        params = (
            cart.customer_id,
            cart.product_id,
            cart.quantity
        )

        cursor.execute(values,params)
        conn.commit()

