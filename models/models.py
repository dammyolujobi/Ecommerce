from sqlalchemy import Column, Integer, String,DOUBLE_PRECISION,DATETIME,Enum,TIMESTAMP,ForeignKey,ARRAY

from config.database import Base
from datetime import datetime,timezone
from schemas.schema import GenderList,Shipping,Payment,Status

class Product(Base):
    __tablename__ = "dim_product"

    id = Column(Integer,primary_key=True,nullable=False,index=True)
    name = Column(String,nullable=False)
    brand = Column(String,nullable=False)
    price = Column(DOUBLE_PRECISION,nullable=False)
    stock_quantity = Column(Integer,nullable=False)
    category = Column(String,nullable=False)
    sub_category = Column(String,nullable=True)
    discount = Column(DOUBLE_PRECISION,nullable=True)
    product_image_url = Column(ARRAY(String),nullable=False)
    date_added = Column(DATETIME,nullable=False,default=datetime.now(timezone.utc))

class Customer(Base):
    __tablename__ = "dim_customers"

    id = Column(Integer,primary_key=True,index=True)
    first_name = Column(String,nullable=False)
    last_name = Column(String,nullable=False)
    email = Column(String,unique=True,nullable=False,index=True)
    gender = Column(Enum(GenderList),nullable=False)
    age = Column(Integer,nullable=False)
    password = Column(String,nullable=False)
    signup_date = Column(DATETIME,nullable = False,default=datetime.now(timezone.utc))

class Date(Base):
    __tablename__ = "dim_date"

    id = Column(Integer,primary_key=True,index=True)
    date = Column(String,nullable=False)
    day = Column(String,nullable=False)
    month = Column(String,nullable=False)
    quarter = Column(Integer,nullable=False)
    year = Column(Integer,nullable=False)
    weekday = Column(Integer,nullable=False)

class Shipping(Base):
    __tablename__ = "dim_shipping"

    id = Column(Integer,primary_key=True,index=True)
    shipping_type = Column(Enum(Shipping),nullable=False)
    shipping_cost = Column(Integer,nullable=False)
    carrier_name = Column(String,nullable=False)
    delivery_time_days = Column(Integer,nullable=False)

class Store(Base):
    __tablename__ = "dim_store"

    id = Column(Integer,primary_key=True,index=True)
    store_name = Column(String,nullable=False)
    location = Column(String,nullable=True)
    manager = Column(String,nullable=False)

class Sales(Base):
    __tablename__ = "fact_sales"

    id = Column(Integer,index=True,primary_key=True)
    customer_id = Column(Integer,ForeignKey("dim_customer.id"))
    product_id = Column(Integer,ForeignKey("dim_product.id"))
    date_id = Column(Integer,ForeignKey("dim_date.id"))
    payment_method = Column(Enum(Payment))
    quantity = Column(Integer,nullable=False)
    sales_status = Column(Enum(Status),nullable = False)
    unit_price = Column(Integer,nullable=False)
    discount = Column(DOUBLE_PRECISION,nullable=False)
    total_amount = Column(DOUBLE_PRECISION,nullable=False)
    sales = Column(Enum(Status),nullable=False)

class GuestCarts(Base):
    __tablename__ = "guest_carts"

    id = Column(Integer,primary_key=True,index=True)
    session_id = Column(String,nullable=False)
    product_id = Column(Integer,ForeignKey("dim_product.id"))
    quantity = Column(Integer,nullable=False)
    expires_at = Column(TIMESTAMP(timezone=True),nullable=False)

class UserCarts(Base):
    __tablename__ = "user_carts"

    id = Column(Integer,primary_key=True,index=True)
    customer_id = Column(Integer,ForeignKey("dim_customers.id"))
    product_id = Column(Integer,ForeignKey("dim_product.id"))
    quantity = Column(Integer,nullable=False)
    
