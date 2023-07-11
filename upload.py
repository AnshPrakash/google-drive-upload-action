#python upload.py <file to upload> <folder name on the drive>

import json
import requests
import os

SCOPES = ["https://www.googleapis.com/auth/drive"]

drive_api = "https://www.googleapis.com/drive"

refresh_token = os.environ['INPUT_REFRESH_TOKEN']
client_id = os.environ['INPUT_CLIENT_ID']
client_secret = os.environ['INPUT_CLIENT_SECRET']


upload_folder = os.environ['INPUT_UPLOAD-FOLDER']
file_to_upload = os.environ['INPUT_FILE-TO-UPLOAD']


def getToken():
    oauth = 'https://www.googleapis.com/oauth2/v4/token' # Google API oauth url
    headers = {'content-type': 'application/x-www-form-urlencoded'}
    data = {
        'grant_type': 'refresh_token',
        'client_id': client_id,
        'client_secret': client_secret,
        'refresh_token': '{}'.format(refresh_token),
    }

    token = requests.post(oauth, headers=headers, data=data)
    _key = json.loads(token.text)
    return _key['access_token']

access_token = getToken()
headers = {"Authorization" : "Bearer {}".format(access_token)}



def upload_file(file_to_upload, upload_folder_id):
    para = {
        "name" : '{}'.format(file_to_upload),
        "parents": ['{}'.format(upload_folder_id)]
    }
    
    files = {
        'data' : ('metadata', json.dumps(para), 'application/json; charset=UTF-8'),
        'file' : open(file_to_upload, "rb")
    }
    response = requests.post("https://www.googleapis.com/upload/drive/v3/files?uploadType=multipart",
        headers = headers,
        files=files
    )
    return response

def getIdFromName(name):
    parameters = {
        "q" : "name : '{entity_name}'".format(entity_name = name)
    }    
    response = requests.get(drive_api+"/v3/files",
        headers = headers,
        params = parameters
    )
    return response

def getFileIdsUnderFolder(folder_id):
    parameters = {
        "q" : "'{id}' in parents".format( id = folder_id)
    }    
    response = requests.get(drive_api+"/v3/files",
        headers = headers,
        params = parameters
    )
    return response

def deleteFileId(id):
    response = requests.delete(drive_api+"/v3/files/{file_id}".format(file_id=id),
        headers = headers,
    )
    return response



def main():
    #get upload_folder_id
    res = getIdFromName(upload_folder)
    upload_folder_id = res.json()['files'][0]['id']

    res = getFileIdsUnderFolder(upload_folder_id)  
    for entity in res.json()['files']:
        if entity['name'] != file_to_upload:
            continue
        id = entity['id']
        deleteFileId(id)
    res = upload_file(file_to_upload, upload_folder_id)
    print(res)
    print(res.json())
    file_id = res.json()['id']
    print(f'::set-output name=file_id::{file_id}')

if __name__ == "__main__":
    main()
