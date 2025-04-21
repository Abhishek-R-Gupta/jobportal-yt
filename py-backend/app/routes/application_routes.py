from flask import Blueprint, request
from app.middlewares.is_authenticated import is_authenticated
from app.controllers.application_controller import (
    apply_job,
    get_applied_jobs,
    get_applicants,
    update_status
)

application_bp = Blueprint('application',__name__)

# Apply to a job by ID
@application_bp.route('/apply/<int:id>', methods=['GET'])
@is_authenticated
def apply(id):
    return apply_job(request,id)

# Get all Jobs the user has applies to 
@application_bp.route('/get',methods=['GET'])
@is_authenticated
def applied_job():
    return get_applied_jobs()


# Get all applicants for a specific job
@application_bp.route('/<int:id>/applicants', methods=['GET'])
@is_authenticated
def applicants(id):
    return get_applicants(id)

# Update application status for a specific application
@application_bp.route('/status/<int:id>/update',methods=['POST'])
@is_authenticated
def updated_application_status(id):
    return update_status(request,id)