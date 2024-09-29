from App.database import db
from .user import User

class Employer(User):
    __tablename__ = 'employers'
    id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
    company_name = db.Column(db.String(100), nullable=False)

    # Set in such a way that if a Employer gets deleted, their job_listings gets deleted as well
    job_listings = db.relationship('Job', backref='employer', lazy=True, cascade="all, delete-orphan")

    __mapper_args__ = {
        'polymorphic_identity': 'employer',
    }

    def __init__(self, username, password, email, company_name):
        super().__init__(username, password, email, user_type='employer')  # Call the parent class constructor
        self.company_name = company_name
