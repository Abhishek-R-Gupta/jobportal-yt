from flask import Blueprint,request
from app.middlewares.is_authenticated import is_authenticated
from app.controllers.job_controller import post_job,get_all_jobs,get_admin_jobs,get_job_by_id

job_bp = Blueprint('job',__name__)

# Route to post a job
@job_bp.route('/post',methods=['POST'])
@is_authenticated
def create_job():
    return post_job(request) 

# Route to get all Jobs
@job_bp.route('/get',methods=['GET'])
@is_authenticated
def fetch_all_jobs():
    return get_all_jobs()

# Route to get a job posted by ADMIN/COMPANY
@job_bp.route('/getadminjobs',methods=['GET'])
@is_authenticated
def fetch_admin_jobs():
    return get_admin_jobs(request)


# Route to Get job by ID
@job_bp.route('/get/<int:id>',methods=['GET'])
@is_authenticated
def fetch_job_by_id(id):
    return get_job_by_id(id)