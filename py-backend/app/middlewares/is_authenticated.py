from functools import wraps
from flask import request, jsonify
import jwt
import os

SECRET_KEY = os.getenv("SECRET_KEY")

def is_authenticated(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        try:
            token = request.cookies.get('token')
            if not token:
                return jsonify({"message":"User not authenticated",'success':False}),401
            
            decoded = jwt.decode(token,SECRET_KEY,algorithms=['HS256'])
            if not decoded:
                return jsonify({"message":'invalid token','sucess':False}), 401
            
            from flask import g
            g.user_id = decoded.get('userId')

            return f(*args,**kwargs)
        
        except jwt.ExpiredSignatureError:
            return jsonify({"message":'token expired','success':False}), 401
        except jwt.InvalidTokenError:
            return jsonify({"message":'invalid token','success':False}), 401
        except Exception as e:
            print(e)
            return jsonify({"message":'Authentication Failed','success':False}), 500
        
    return decorated_function