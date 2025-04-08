from app import db
from datetime import datetime
import time

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    fullname = db.Column(db.String(100),nullable=False)
    email = db.Column(db.String(100),unique=True, nullable=False)
    phone_number = db.Column(db.String(20),nullable=False)
    password = db.Column(db.String(255),nullable=False)

    role = db.Column(db.String(20), nullable=False)

    #Profile Fields
    bio = db.Column(db.Text, nullable=True)
    skills = db.Column(db.PickleType,nullable=True) # stores list of skills
    resume = db.Column(db.String(255), nullable=True) # url for resume
    resume_original_name = db.Column(db.String(255), nullable=True)

    company_id = db.Column(db.Integer,db.ForeignKey('companies.id'),nullable=True)
    company = db.relationship('Company',backref = 'users')

    profile_photo = db.Column(db.String(255),default='')

    created_at = db.Column(db.DateTime,default=datetime.utcnow())
    updated_at = db.Column(db.DateTime,default=datetime.utcnow(), onupdate=datetime.utcnow())