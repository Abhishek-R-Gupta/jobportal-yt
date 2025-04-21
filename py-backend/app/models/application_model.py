from app.utils.db import db
from datetime import datetime

class Application(db.Model):
    __tablename__ = 'applications'

    id = db.Column(db.Integer,primary_key=True)

    job_id = db.Column(db.Integer,db.ForeignKey('jobs.id'),nullable=False)
    applicant_id = db.Column(db.Integer,db.ForeignKey('users.id'),nullable=False)

    status = db.Column(db.Enum('pending','accepted','rejected'),default='pending',nullable=False)

    created_at = db.Column(db.DateTime,default=datetime.utcnow,nullable=False)
    updated_at = db.Column(db.DateTime,default=datetime.utcnow,nullable=False,onupdate=datetime.utcnow)

    # relationships
    job = db.relationship('Job',back_populates='applications')
    applicant = db.relationship('User',back_populates='applications')

    def serialize(self):
        return {
            "id": self.id,
            "status": self.status,
            "created_at": self.created_at.isoformat()
        }

    def serialize_with_job(self):
        return {
            "id": self.id,
            "status": self.status,
            "created_at": self.created_at.isoformat(),
            "job": self.job.serialize_basic() if self.job else None
        }

    def serialize_with_applicant(self):
        return {
            "id": self.id,
            "status": self.status,
            "created_at": self.created_at.isoformat(),
            "applicant": self.applicant.serialize_basic() if self.applicant else None
        }