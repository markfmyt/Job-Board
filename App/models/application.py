from App.database import db

class Application(db.Model):
    __tablename__ = 'applications'
    application_id = db.Column(db.Integer, primary_key=True)
    job_seeker_id = db.Column(db.Integer, db.ForeignKey('job_seekers.id'), nullable=False)
    job_id = db.Column(db.Integer, db.ForeignKey('jobs.id'), nullable=False)
    application_text = db.Column(db.Text, nullable=False)
    is_accepted = db.Column(db.Boolean, default=None, nullable=True)

    def __repr__(self):
        return f'<Application {self.application_id} by JobSeeker {self.job_seeker_id} for Job {self.job_id}>'
