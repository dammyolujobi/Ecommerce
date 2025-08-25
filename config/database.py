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


DATABASE_URL = f"postgresql+psycopg2://{username}:{encoded_password}@{host}:{port}/{database}"

engine = create_engine(DATABASE_URL,echo=True)

Base = declarative_base()

SessionLocal = sessionmaker(bind=engine)

