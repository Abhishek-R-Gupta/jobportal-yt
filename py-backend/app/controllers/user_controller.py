from flask import jsonify, request, make_response
from app.models.user_model import User,db
from app.utils.cloudinary import upload_to_cloudinary
from app.utils.datauri import get_data_uri
from werkzeug.security import generate_password_hash, check_password_hash
import jwt, os
from datetime import datetime, timedelta

SECRET_KEY = os.getenv('SECRET_KEY')

def register(req):
    try:
        data = req.form
        file = req.file

        fullname = data.get('fullname')
        email = data.get('email')
        phoneNumber = data.get('phoneNumber')
        password = data.get('password')
        role = data.get('role')


        print(f'{fullname} \t {email} \t {phoneNumber} \t {password} \t {role}')

        if not all([fullname,email,phoneNumber,password,role]):
            return jsonify({'message':"Something is missing","success":False}),400
        existing_user = User.query.filter_by(email=email).frst()
        if existing_user:
            return jsonify({'message':'User already exists with this email.','success':False}), 400
        
        file_uri = get_data_uri(file)
        cloud_response= upload_to_cloudinary(file_uri['content'])

        hashed_password = generate_password_hash(password)

        new_user = User(
            fullname = fullname,
            email = email,
            phoneNumber = phoneNumber,
            passwpord = password,
            role = role,
            profilePhoto = cloud_response["secure_url"]
        )

        db.session.add(new_user)
        db.session.commit()

        return jsonify({'message':"Account Created Successfully.", 'success':True}),201
    except Exception as e:
        print(e)
        return jsonify({'message':'Registration Failed','success':False}), 500



def login(req):
    try:
        data = req.get_json()
        email = data.get("email")
        password = data.get('password')
        role = data.get('role')

        if not all([email,password,role]):
            return jsonify({'message':'Soemthing is missing','success':False}),400
        
        user = User.query.filter_by(email=email).first()

        if not  user or not check_password_hash(user.password, password):
            return jsonify({'message':'Invalid email or password.','success':False}), 400
        
        if role != user.role:
            return jsonify({"message":"Account not found for this role",'success':False}),400
        
        token_payload = {"userId":str(user.id),'exp':datetime.utcnow()+timedelta(days=1)}
        token = jwt.encode(token_payload,SECRET_KEY,algorithm='HS256')

        user_data = {
            'id':user.id,
            'fullname':user.fullname,
            'email':user.email,
            'phoneNumber':user.phoneNumber,
            'role':user.role,
            'profilePhoto':user.profilePhoto,
            'bio':user.bio,
            'skills':user.skills,
            'resume':user.resume,
            'resumeOriginalName':user.resumeOriginalName
        }

        response = make_response(jsonify({'message':'f"welcome back {user.fullname}','user':user_data,'success':True}))
        response.set_cookie('token',token,max_age=86400,httponly=True,samesit='Strict')

        return response
    except Exception as e:
        print(e)
        return jsonify({"message":'Login Failed.','success':False}),500
    

def logout():
    response = make_response(jsonify({"message":"logged out successfully",'success':True}))
    response.set_cookie('token',"",max_age=0)
    return response

def update_profile(req):
    try:
        user_id = req.id
        data = req.form
        file = req.file

        user = User.query.get(user_id)
        if not user:
            return jsonify({"message":"user not found"})
    
        if data.get('fullname'): user.fullname = data['fullname']
        if data.get('email'): user.email = data['email']
        if data.get('phoneNumber'): user.phoneNumber = data['phoneNumber']
        if data.get('bio'):user.bio = data['bio']
        if data.get('skills'): user.skills = [s.strip() for s in data['skills'].split(',')]

        if file:
            file_uri = get_data_uri(file)
            cloud_response = upload_to_cloudinary(file_uri['content'])
            user.resume = cloud_response['secure_uri']
            user.resumeOriginalName = file.filename

        db.session.commit()

        updated_user = {
            'id':user.id,
            'fullname':user.fullname,
            'email':user.email,
            'phoneNumber':user.phoneNumber,
            'role':user.role,
            'profilePhoto':user.profilePhoto,
            'bio':user.bio,
            'skills':user.skills,
            'resume':user.resume,
            'resumeOriginalName':user.resumeOriginalName
        }

        return jsonify({'message':'profile updated successfully.','user':updated_user,'success':True})
    
    except Exception as e:
        print(e)
        return jsonify({"message":'Profile update failed.','success':False}) , 500