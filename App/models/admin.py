from App.database import db
from .user import User

class Admin(User):
    __tablename__ = 'admins'
    id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)

    __mapper_args__ = {
        'polymorphic_identity': 'admin',
    }

    def __init__(self, username, password, email):
        super().__init__(username, password, email, user_type='admin')  # Call the parent class constructor
