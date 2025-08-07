from fastapi import Depends,APIRouter,HTTPException,status
from schemas.schema import CustomerBase
import bcrypt
from jose import jwt
from jose import JWTError
from fastapi.security import OAuth2PasswordBearer
from utils.utils import auth_password,create_access_token,create_refresh_token
from config.database import conn,cursor
from dotenv import load_dotenv
import os

SECRET_KEY = os.getenv("JWT_SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

# Create router
router = APIRouter(
    prefix="/users"
)

# Create user
@router.post("/create_user")
async def create_user(customer:CustomerBase = Depends()):

    # Store retrieved emails
    Email = []
    # Hashing Password
    salt = bcrypt.gensalt()
    password = customer.password.encode('utf-8')

    hashed_password = bcrypt.hashpw(password,salt).decode('utf-8')
    gender = str(customer.gender.value) if hasattr(customer.gender,'value') else str(customer.gender)

    values = ("""
        INSERT INTO dim_customers(first_name,last_name,email,gender,age,password)
        VALUES(%s,%s,%s,%s,%s,%s)
                   """)
    # Check for existing password in database
    check = """
        SELECT * FROM dim_customers
        WHERE email = %s
            """
    cursor.execute(check,(customer.email,))
    result = cursor.fetchone()
    if result:
        return "This user has been registered already"
    
    

    params = (
        customer.first_name,
        customer.last_name,
        customer.email,
        gender,
        customer.age,
        hashed_password
    )
    
    cursor.execute(values,params)
    conn.commit()

    return "Successfully created"

@router.post("/login")
async def login_user(email:str,password:str):  
          
    check_email = """
        SELECT * FROM dim_customers
        WHERE email = %s
            """
    cursor.execute(check_email,(email,))
    confirmed_email = cursor.fetchone()

    check_password = """
        SELECT password FROM dim_customers
        WHERE email = %s
                    """
    cursor.execute(check_password,(email,))
    confirmed_password = cursor.fetchone()
    
    if confirmed_email:
        if auth_password(password,confirmed_password["password"]):
            return {
                "access token": create_access_token(confirmed_email),
                "refresh_token": create_refresh_token(confirmed_email)
            }
    else:
        return "Wrong email or password"

def get_current_user(token:str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"}
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        return credentials_exception

@router.get("/users/me")
def read_users(current_user:str = Depends(get_current_user)):
    return {"user":current_user}