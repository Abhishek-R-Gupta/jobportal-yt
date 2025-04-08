import base64
import mimetypes

def get_data_uri(file):
    file_content = file.read()
    mime_type = mimetypes.guess_type(file.filename)[0]

    if not mime_type:
        mime_type = 'application/octet-stream'

    base64_encoded = base64.b64encode(file_content).decode('utf-8')
    data_uri = f'data:{mime_type};base64,{base64_encoded}'

    return{
        'content':data_uri,
        'filename':file.filename,
        'mimetype':mime_type
    }