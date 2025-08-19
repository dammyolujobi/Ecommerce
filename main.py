from fastapi import FastAPI,UploadFile,File,Depends
from config.database import SessionLocal
from models.models import Product
from schemas.schema import ProductBase
from routers.users import router
from typing import List
from sqlalchemy import func
import os
from dotenv import load_dotenv
from config.google_configuration import upload_for_url

load_dotenv()

# Initialized router
app = FastAPI()


app.include_router(router=router)

#List of file types
filetypes = ["jpeg","png"]

#Initialize Session
session = SessionLocal()

#Get the google folder id for uploading
folder_id = os.getenv("FOLDER_ID")


@app.post("/users/add/product")
async def add_product_values(product: ProductBase = Depends(),files: List[UploadFile] = File(...)):
   file_urls = [] # Store for urls
   
   for file in files:
      file_url =  await upload_for_url(file,folder_id=folder_id)
      file_urls.append(file_url)

   try:
      add_product = Product(**product.model_dump(),
                            product_image_url = file_urls)
      
      session.add(add_product)
      session.commit()
      session.refresh(add_product)
      return "Succesfully Uploaded"
   
   except RuntimeError as e:
      return "e"


@app.get("/retrieve-products")
async def retrieve_products(name:str):
   product = session.query(Product).filter(func.lower(Product.name).like(f"%{name.lower()}%")).all()
   return product
