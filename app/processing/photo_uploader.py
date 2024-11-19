def upload_photo(service, file_path, folder_id):
    file_metadata = {'name': file_path, 'parents': [folder_id]}
    media = MediaFileUpload(file_path, mimetype='image/png')
    file = service.files().create(body=file_metadata, media_body=media).execute()
    return file.get('id')
