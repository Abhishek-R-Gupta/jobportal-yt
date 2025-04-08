from flask import Blueprint, request
from app.controllers.user_controller import register, login, logout, update_profile
from app.middlewares.is_authenticated import is_authenticated
from app.middlewares.file_upload import single_file_required

user_bp = Blueprint('user',__name__)

#/api/v1/user/registration
@user_bp.route('/register',methods=['POST'])
@single_file_required
def register_user():
    return register(request)

# /api/v1/user/Login
@user_bp.route('/login',methods=['POST'])
def login_user():
    return login(request)

# /api/v1/user/Logout
@user_bp.route('/logout',methods = ['GET'])
def logout_user():
    return logout()

# /api/v1/user/profile/update
@user_bp.route('/profile/update',methods = ['POST'])
@is_authenticated
@single_file_required
def update_user_profile():
    return update_profile(request)