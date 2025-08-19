from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base,sessionmaker
from urllib.parse import quote_plus
from dotenv import load_dotenv
import os

load_dotenv()

password =os.getenv("PASSWORD")

encoded_password = quote_plus(password)

DATABASE_URL = f"postgresql+psycopg2://postgres:{encoded_password}@localhost:5432/E-COMMERCE"

engine = create_engine(DATABASE_URL,echo=True)

Base = declarative_base()

SessionLocal = sessionmaker(bind=engine)

