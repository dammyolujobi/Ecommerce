from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload,HttpError
import mimetypes
import tempfile
import shutil
from fastapi import File,UploadFile,Depends


# Drive API scopes
SCOPES = ["https://www.googleapis.com/auth/drive"]

creds = Credentials.from_authorized_user_file("token.json",SCOPES)

service = build("drive", "v3", credentials=creds)

async def upload_for_url(file_detail:UploadFile = File(...), folder_id:str = Depends())->str:
    try:
        
        with tempfile.NamedTemporaryFile(delete=False,suffix=file_detail.filename) as tmp:
            shutil.copyfileobj(file_detail.file, tmp)
            temp_path = tmp.name

        mime,_ =  mimetypes.guess_file_type(temp_path)
        file_metadata = {
            "name": file_detail.filename,
            "parents":[folder_id]
            }

        media = MediaFileUpload(
            temp_path,
            mimetype=mime,
            )
        file = (
            service.files().
            create(body = file_metadata,media_body = media,fields = "id")
            .execute()
        )

        file_id = file["id"]
        
        return f"https://drive.google.com/file/d/{file_id}/view?usp=sharing"

    except HttpError as e:
        return e.error_details