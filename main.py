from fastapi import FastAPI,UploadFile,File,Depends
from fastapi.responses import JSONResponse
from config.database import conn
from psycopg2 import Binary
from config.database import cursor
from schemas.schema import ProductBase
from routers.users import router
import base64


# Initialized router
app = FastAPI()

app.include_router(router=router)

#List of file types
filetypes = ["jpeg","png"]

# Get Products model
@app.post("/product")
async def add_product_values(product: ProductBase = Depends(),file:UploadFile = File(...)):
   try:
    content = await file.read()
    
        
    insert = ("""
            INSERT INTO dim_product(name,brand,price,stock_quantity,category,sub_category,product_image)
            VALUES(%s,%s,%s,%s,%s,%s,%s)
            RETURNING id;
                    """)
    
    params = (
      product.name,
      product.brand,
      product.price,
      product.stock_quantity,
      product.category,
      product.subcategory,
      Binary(content)
      
      )
    
    cursor.execute(insert,params)
    conn.commit()
    return "Succesfully Uploaded"
   except RuntimeError as e:
      return "e"


@app.get("/retrieve-products")
async def retrieve_products(name:str):
    search = """
    SELECT * FROM dim_product
    WHERE name ILIKE %s;
    """
    search_pattern = f"%{name}%"
    cursor.execute(search,(search_pattern,))
    results = cursor.fetchall()
    
    for row in results:
       for key, value in row.items():
          if isinstance(value,memoryview):
            row[key] = base64.b64encode(value).decode("utf-8")


    return JSONResponse(results)
