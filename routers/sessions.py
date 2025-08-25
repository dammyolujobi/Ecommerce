from fastapi import APIRouter,Request,Response,Cookie
import secrets

def get_or_create_session_id(request:Request,response:Response,session_id:str = Cookie(default=None)):
    if not session_id:
        session_id = secrets.token_hex(16)
        response.set_cookie(key="session_id", value=session_id,httponly=True)

    return session_id

get_or_create_session_id(Request,Response)