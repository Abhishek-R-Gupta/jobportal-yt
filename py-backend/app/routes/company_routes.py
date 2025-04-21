from flask import Blueprint,request
from app.middlewares.is_authenticated import is_authenticated
from app.controllers.company_controller import (
    register_company,
    get_company,
    get_company_by_id,
    update_company
)
from app.middlewares.file_upload import single_file_required

company_bp = Blueprint('company',__name__)

# Route to regester a company
@company_bp.route('/register',methods=['POST'])
@is_authenticated
def register():
    return register_company(request)

# Route to get company info (of authenticated user)
@company_bp.route('/get',methods=['GET'])
@is_authenticated
def get_user_company():
    return get_company()

# Route to get company info by id
@company_bp.route('/get/<int:id>',methods=['GET'])
@is_authenticated
def get_by_id(id):
    return get_company_by_id(id)

# Route to update company info
@company_bp.route('/update/<int:id>',methods=['PUT'])
@is_authenticated
@single_file_required
def update(id):
    return update_company(request,id)