from flask import request, jsonify
# import pandas as pd
from app.utils import db
from flask_jwt_extended import get_jwt_identity
from utils.cloudinary import upload_to_cloudinary
from app.models import company_model

# ✅ Register company
def register_company():
    try:
        data = request.form or request.json
        company_name = data.get("companyName")

        if not company_name:
            return jsonify({"message": "Company name is required.", "success": False}), 400

        existing = company_model.query.filter_by(name=company_name).first()
        if existing:
            return jsonify({"message": "You can't register same company.", "success": False}), 400

        company = company_model(name=company_name, user_id=get_jwt_identity())
        db.session.add(company)
        db.session.commit()

        return jsonify({"message": "Company registered successfully.", "company": company.serialize(), "success": True}), 201

    except Exception as e:
        print(e)
        return jsonify({"message": "Server Error", "success": False}), 500

# ✅ Get all companies of logged-in user
def get_company():
    try:
        user_id = get_jwt_identity()
        companies = company_model.query.filter_by(user_id=user_id).all()

        if not companies:
            return jsonify({"message": "Companies not found.", "success": False}), 404

        return jsonify({"companies": [c.serialize() for c in companies], "success": True}), 200

    except Exception as e:
        print(e)
        return jsonify({"message": "Server Error", "success": False}), 500

# ✅ Get company by ID
def get_company_by_id(company_id):
    try:
        company = company_model.query.get(company_id)

        if not company:
            return jsonify({"message": "Company not found.", "success": False}), 404

        return jsonify({"company": company.serialize(), "success": True}), 200

    except Exception as e:
        print(e)
        return jsonify({"message": "Server Error", "success": False}), 500

# ✅ Update company
def update_company(company_id):
    try:
        data = request.form or request.json
        name = data.get("name")
        description = data.get("description")
        website = data.get("website")
        location = data.get("location")
        logo = None

        # Check file upload
        if 'file' in request.files:
            file = request.files['file']
            cloud_response = upload_to_cloudinary(file)
            logo = cloud_response['secure_url']

        update_data = {}
        if name: update_data['name'] = name
        if description: update_data['description'] = description
        if website: update_data['website'] = website
        if location: update_data['location'] = location
        if logo: update_data['logo'] = logo

        company = company_model.query.get(company_id)
        if not company:
            return jsonify({"message": "Company not found.", "success": False}), 404

        for key, value in update_data.items():
            setattr(company, key, value)

        db.session.commit()

        return jsonify({"message": "Company information updated.", "success": True}), 200

    except Exception as e:
        print(e)
        return jsonify({"message": "Server Error", "success": False}), 500
