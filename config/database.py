from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base,sessionmaker
from urllib.parse import quote_plus
from dotenv import load_dotenv
import os

load_dotenv()

password =os.getenv("PASSWORD")
port = os.getenv("DB_PORT")
database = os.getenv("DATABASE")
username = os.getenv("DB_USERNAME")
host = os.getenv("HOSTNAME")
encoded_password = quote_plus(password)


DATABASE_URL = "postgresql://user:O6MSN4DgKiz7mxGMUCqczUlssLzm41MV@dpg-d2m8bore5dus739hr070-a.oregon-postgres.render.com/ecommerce_l0c4"

engine = create_engine(
    DATABASE_URL,
    echo=True,
    pool_pre_ping=True
    )

Base = declarative_base()

SessionLocal = sessionmaker(bind=engine)

Base.metadata.create_all(bind=engine)