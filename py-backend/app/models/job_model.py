from app.utils.db import db
from datetime import datetime

class Job(db.Model):
    __tablename__ = 'jobs'

    id = db.Column(db.Integer,primary_key = True)
    title = db.Column(db.String(255),nullable = False)
    description = db.Column(db.Text,nullable = False)
    requirements = db.Column(db.JSON)
    salary = db.Column(db.Float, nullable = False)
    experience_level = db.Column(db.Integer,nullable = False)
    location = db.Column(db.String(255),nullable = False)
    job_type = db.Column(db.String(100),nullable = False)
    position = db.Column(db.Integer,nullable = False)

    company_id = db.Column(db.Integer,db.ForeignKey('companies.id'), nullable = False)
    created_by_id = db.Column(db.Integer,db.ForeignKey('users.id'),nullable=False)

    created_at = db.Column(db.DateTime, default = datetime.utcnow)
    updated_at= db.Column(db.DateTime,default = datetime.utcnow,onupdate = datetime.utcnow)

    # relationships 
    company = db.relationship('Company',back_populates = 'jobs')
    created_by = db.relationship('User',back_populates = 'jobs_posted')
    applications = db.relationship('Application',back_populates='job',cascade='all, delete-orphan')

    def serialize(self):
        return {
            "id": self.id,
            "title": self.title,
            "location": self.location,
            "salary": self.salary,
            "job_type": self.job_type,
            "experience_level": self.experience_level,
            "position": self.position,
            "created_at": self.created_at.isoformat(),
            "company": self.company.serialize_basic() if self.company else None
        }