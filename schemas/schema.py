from pydantic import BaseModel
from enum import Enum
from typing import Optional,List

class ProductBase(BaseModel):
    name:str
    brand:str
    price:int
    stock_quantity:int
    category:str
    sub_category:str
    discount:float
    

class Shipping(Enum):
    standard = "standard"
    express = "express"
    same_day = "same-day"

class GenderList(Enum):
    male = "male"
    female= "female"

class Payment(Enum):
    credit = "credit_card"
    transfer = "bank_transfer"

class Status(Enum):
    completed = "completed" 
    cancelled = "cancelled"
    refunded = "refunded"
class CustomerBase(BaseModel):
    first_name:str
    last_name:str
    email:str
    gender:GenderList
    age:int
    password:str

class DateBase(BaseModel):
    date:str
    day:str
    month:str
    quarter:int
    year:int
    weekday:int

class ShippingBase(BaseModel):
    shipping_type:Shipping
    shipping_cost:int
    carrier_name:str
    delivery_time_days:int

class StoreBase(BaseModel):
    store_name:str
    location:str
    manager:str

class SalesBase(BaseModel):
    customer_id:int
    product_id:int
    date_id:int
    payment_method:Payment
    quantity:int
    unit_price:int
    dicount:int
    total_amount:int
    status:Status

class CartBase(BaseModel):
    customer_id:Optional[int] = None 
    session_id:Optional[int] = None
    quantity:int
    product_id:int

