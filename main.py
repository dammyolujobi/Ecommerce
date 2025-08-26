from fastapi import FastAPI,UploadFile,File,Depends
from config.database import SessionLocal
from models.models import Product
from schemas.schema import ProductBase
from routers import checkout, sales,store,users,location,payment
from typing import List
from sqlalchemy import func
import uvicorn
import os
from dotenv import load_dotenv
from config.drive_configuration import upload_for_url
from config.get_drive_id_for_folder import create_folder
from routers.users import oauth2_scheme

load_dotenv()

# Initialized router
app = FastAPI(
   title="E-commerce Api"

)


app.include_router(sales.router)
app.include_router(store.router)
app.include_router(users.router)
app.include_router(location.router)
app.include_router(checkout.router)
app.include_router(payment.router)

#List of file types
filetypes = ["jpeg","png"]

#Initialize Session
session = SessionLocal()

#Get the google folder id for uploading
folder_id = create_folder()


@app.post("/users/add/product")
async def add_product_values(product: ProductBase = Depends(),files: List[UploadFile] = File(...),authenticate:str = Depends(oauth2_scheme)):
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

if __name__ == "__main__":
   uvicorn.run(port=8000,reload=True,app="main:app",host="0.0.0.0")