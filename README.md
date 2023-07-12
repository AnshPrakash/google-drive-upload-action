# Google Drive file upload docker action

This action uploads a file to Google Drive

## Inputs

## `client_id`
**Required** Client_id of the Google App.


## `client_secret`
**Required** Client_secret of the Google App.


## `refresh_token`
**Required** refresh token acquired for a particular user on whose drive you want to upload.


## `file-to-upload`
**Required** Name of the file to upload.


## `upload-folder`
**Required** Drive folder name where file is to be uploaded.



## Outputs

## `file_id`

File_id of the uploaded file on Google drive.

## Example usage
```
uses: AnshPrakash/google-drive-upload-action@main
with:
    client_id: ${{ secrets.CLIENT_ID }}
    client_secret: ${{ secrets.CLIENT_SECRET }}
    refresh_token: ${{ secrets.REFRESH_TOKEN }}
    file-to-upload: 'file.txt'
    upload-folder: 'some-folder-on-google-drive'
```
