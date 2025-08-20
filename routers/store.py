from fastapi import APIRouter
from schemas.schema import StoreBase
from models.models import Store
from config.database import SessionLocal

session = SessionLocal()

router = APIRouter(
    prefix="/company"
)

@router.post("/store")
async def add_store(store:StoreBase):
    add_store = Store(**store.model_dump)
    session.add(add_store)
    session.commit()
    session.refresh(add_store)

    return add_store

