from App.database import db
from .user import User

class JobSeeker(User):
    __tablename__ = 'job_seekers'
    id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
    applications = db.relationship('Application', backref='job_seeker', lazy=True, cascade="all, delete-orphan")

    __mapper_args__ = {
        'polymorphic_identity': 'job_seeker',
    }

    def __init__(self, username, password, email):
        super().__init__(username, password, email, user_type='job_seeker')  # Call the parent class constructor
