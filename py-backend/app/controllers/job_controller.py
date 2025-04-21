from flask import request,jsonify
from app.models import job_model, company_model, application_model
from app.utils import db
from sqlalchemy import or_
from flask_jwt_extended import get_jwt_identity 

# Admin posts job
def post_job():
    try:
        data = request.json
        title = data.get('title')
        description = data.get('description')
        requirements = data.get('requirements')
        salary = data.get('salary')
        location = data.get('location')
        job_type = data.get('jobType')
        experience = data.get('experience')
        position = data.get('position')
        company_id = data.get('companyId')
        user_id = get_jwt_identity()

        if not all([title,description,requirements,salary,location,job_type,experience,position,company_id]):
            return jsonify({'message': 'Something is Missing','success':False}), 400
        
        job = job_model(
            title=title,
            description=description,
            requirements=requirements.split(","),
            salary=salary,
            location=location,
            job_type=job_type,
            experience_level= experience,
            position=position,
            company_id=company_id,
            created_by = user_id
        )
        db.session.add(job)
        db.session.commit()

        return jsonify({"message":'New Job Created Successfully.','job':job.serialize(),'success':True}) , 201
    
    except Exception as e:
        print(e)
        return jsonify({'message': 'Server error','success':False}), 500
    

# for student:get all jobs
def get_all_jobs():
    try:
        keyword = request.args.get("keyword", "")
        jobs = job_model.query.filter(
            or_(
                job_model.title.ilike(f"%{keyword}%"),
                job_model.description.ilike(f"%{keyword}%")
            )
        ).order_by(job_model.created_at.desc()).all()

        if not jobs:
            return jsonify({"message": "Jobs not found.", "success": False}), 404

        return jsonify({"jobs": [job.serialize() for job in jobs], "success": True}), 200

    except Exception as e:
        print(e)
        return jsonify({"message": "Server Error", "success": False}), 500


# For student: Get job by ID
def get_job_by_id(job_id):
    try:
        job = job_model.query.filter_by(id=job_id).first()

        if not job:
            return jsonify({"message": "Job not found.", "success": False}), 404

        return jsonify({"job": job.serialize(include_applications=True), "success": True}), 200

    except Exception as e:
        print(e)
        return jsonify({"message": "Server Error", "success": False}), 500


# For admin: Get admin jobs
def get_admin_jobs():
    try:
        admin_id = get_jwt_identity()
        jobs = job_model.query.filter_by(created_by=admin_id).order_by(job_model.created_at.desc()).all()

        if not jobs:
            return jsonify({"message": "Jobs not found.", "success": False}), 404

        return jsonify({"jobs": [job.serialize() for job in jobs], "success": True}), 200

    except Exception as e:
        print(e)
        return jsonify({"message": "Server Error", "success": False}), 500