from fastapi import Depends,APIRouter,HTTPException,status
from schemas.schema import CustomerBase
import bcrypt
from typing import Annotated
from jose import jwt
from jose import JWTError
from fastapi.security import OAuth2PasswordBearer,OAuth2PasswordRequestForm
from utils.utils import auth_password,create_access_token,create_refresh_token
from models.models import Customer
from config.database import SessionLocal
import os

SECRET_KEY = os.getenv("JWT_SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")

#Initial session
session = SessionLocal()


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/users/login")

# Create router
router = APIRouter(
    prefix="/users",
    tags=["users"]
)

# Create user
@router.post("/create_user")
async def create_user(customer:CustomerBase = Depends()):

    password = customer.password.encode('utf-8')
    hashed_password = bcrypt.hashpw(password,bcrypt.gensalt()).decode('utf-8')

    gender = str(customer.gender.value) if hasattr(customer.gender,'value') else str(customer.gender)

    add_customer = Customer(
        first_name = customer.first_name,
        last_name = customer.last_name,
        email = customer.email,
        gender = gender,
        age = customer.age,
        password = hashed_password
    )
    
    check_email = session.query(Customer).filter(Customer.email == customer.email).first()
    if check_email:
        return "This email has been registered already"
    else:
        session.add(add_customer)
        session.commit()
        session.refresh(add_customer)

        return "Successfully created"


@router.post("/login")
async def login(login: Annotated[OAuth2PasswordRequestForm, Depends()]):  
    confirmed_user = session.query(Customer).filter(Customer.email == login.username).first()
    
    confirmed_password = confirmed_user.password

    user_name = confirmed_user.first_name

    if confirmed_user:
        if auth_password(login.password,confirmed_password):
            return {
                "access_token": create_access_token(user_name),
                "refresh_token": create_refresh_token(user_name)
            }
    else:
        return "Wrong email or password"

@router.post("/get_current_user")
async def get_current_user(token:str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"}
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=ALGORITHM)
        return payload["sub"]
    
    except JWTError:
        raise credentials_exception




