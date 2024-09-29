from datetime import datetime
from App.database import db

class Job(db.Model):
    __tablename__ = 'jobs'
    id = db.Column(db.Integer, primary_key=True)
    category = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    date_posted = db.Column(db.DateTime, default=datetime.utcnow)
    employer_id = db.Column(db.Integer, db.ForeignKey('employers.id'), nullable=False)

    # Set in such a way that if a Job gets deleted, all the applications for that job gets deleted as well
    applications = db.relationship('Application', backref='job', lazy=True, cascade="all, delete-orphan")
