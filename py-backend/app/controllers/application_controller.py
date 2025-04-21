from flask import request, jsonify
from flask_jwt_extended import get_jwt_identity
from app.models import  job_model, application_model, user_model  # Ensure your models are correctly defined and imported
from app.utils import db


# Apply for a job
def apply_job(job_id):
    try:
        user_id = get_jwt_identity()

        if not job_id:
            return jsonify({"message": "Job id is required.", "success": False}), 400

        existing = application_model.query.filter_by(job_id=job_id, applicant_id=user_id).first()
        if existing:
            return jsonify({"message": "You have already applied for this job", "success": False}), 400

        job = job_model.query.get(job_id)
        if not job:
            return jsonify({"message": "Job not found", "success": False}), 404

        application = application_model(job_id=job_id, applicant_id=user_id)
        db.session.add(application)
        db.session.commit()

        return jsonify({"message": "Job applied successfully.", "success": True}), 201

    except Exception as e:
        print(e)
        return jsonify({"message": "Server error", "success": False}), 500


# Get all jobs applied by a user
def get_applied_jobs():
    try:
        user_id = get_jwt_identity()
        applications = application_model.query.filter_by(applicant_id=user_id).order_by(application_model.created_at.desc()).all()

        if not applications:
            return jsonify({"message": "No Applications", "success": False}), 404

        data = [a.serialize_with_job() for a in applications]  # Make sure you have a `serialize_with_job` method

        return jsonify({"application": data, "success": True}), 200

    except Exception as e:
        print(e)
        return jsonify({"message": "Server error", "success": False}), 500


# Admin can see all applicants for a job
def get_applicants(job_id):
    try:
        job = job_model.query.get(job_id)
        if not job:
            return jsonify({"message": "Job not found.", "success": False}), 404

        applications = application_model.query.filter_by(job_id=job_id).order_by(application_model.created_at.desc()).all()
        data = [a.serialize_with_applicant() for a in applications]  # Ensure this method exists

        return jsonify({"job_id": job_id, "applications": data, "success": True}), 200

    except Exception as e:
        print(e)
        return jsonify({"message": "Server error", "success": False}), 500


# Update the status of an application
def update_status(application_id):
    try:
        status = request.json.get("status")
        if not status:
            return jsonify({"message": "Status is required", "success": False}), 400

        application = application_model.query.get(application_id)
        if not application:
            return jsonify({"message": "Application not found.", "success": False}), 404

        application.status = status.lower()
        db.session.commit()

        return jsonify({"message": "Status updated successfully.", "success": True}), 200

    except Exception as e:
        print(e)
        return jsonify({"message": "Server error", "success": False}), 500
