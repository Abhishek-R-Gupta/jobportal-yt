from functools import wraps
from flask import request, jsonify

def single_file_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'file' not in request.files:
            return jsonify({"message":'File is missing','success':False}), 400
        
        file = request.files['files']
        if file.filename == "":
            return jsonify({"message":'no file is selected','success':False}), 400
        
        request.file = file
        return f(*args, **kwargs)

    return decorated_function