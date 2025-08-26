from config.drive_configuration import service
from googleapiclient.http import HttpError

def create_folder():
    try:
      """ Create a folder and prints the folder ID
        Returns : Folder Id 
        Load pre-authorized user credentials from the environment. """

      file_metadata = {
          "name": "Photos of Products",
          "mimeType": "application/vnd.google-apps.folder"
      }
      folder_name = file_metadata["name"]

      # Check for existing folder with the given nam
      check = service.files().list(
        q= f"name='{folder_name}' and mimeType='application/vnd.google-apps.folder' and trashed=false",
        fields="files(id, name)"
        ).execute()
      
      item = check.get('files',[])

      if item:
          print("Folder already exists")
      
      else:
        file = service.files().create(body=file_metadata, fields="id").execute()
        
        print(file.get("id"))

    except HttpError as e:
       print(e.error_details)

