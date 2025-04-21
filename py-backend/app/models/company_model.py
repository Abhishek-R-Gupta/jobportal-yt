from utils.db import db
from datetime import datetime

class Company(db.Model):
    __tablename__ = 'companies'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255),nullable = False,unique=True)
    description = db.Column(db.Text)
    website = db.Column(db.String(255))
    location = db.Column(db.String(255))
    logo = db.Column(db.String(512)) # logo url

    user_id = db.Column(db.Integer,db.ForeignKey('users.id'),nullable=False)

    created_at = db.Column(db.DateTime,default=datetime.utcnow)
    updated_at = db.Column(db.DateTime,default=datetime.utcnow,onupdate=datetime.utcnow)

    #relationships
    user=db.relationship('User',back_populates='companies')
    jobs = db.relationship('Job',back_populates='company',cascade='all, delete-orphan')
    

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "website": self.website,
            "location": self.location,
            "logo": self.logo,
            "user_id": self.user_id
        }
