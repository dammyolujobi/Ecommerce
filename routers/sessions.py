from fastapi import APIRouter,Request,Response
import secrets

def get_or_create_session_id(request:Request,response:Response):
    session_id = request.cookies.get("session_id")
    if not session_id:
        session_id = secrets.token_hex(16)
        response.set_cookie(key="session_id", value=session_id,httponly=True)
    return session_id