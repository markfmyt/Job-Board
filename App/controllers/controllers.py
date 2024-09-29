from App.models import db, User, Admin, Employer, JobSeeker, Job, Application
from werkzeug.security import generate_password_hash, check_password_hash

# Controller functions

# Controller function to create a user with specified role [ALL USERS]
def create_user(username, password, email, role):
    hashed_password = generate_password_hash(password)  # Replace with your hashing logic
    if role == 'employer':
        user = Employer(username=username, password=hashed_password, email=email, company_name="DefaultCompany")
    elif role == 'job_seeker':
        user = JobSeeker(username=username, password=hashed_password, email=email)
    elif role == 'admin':
        user = Admin(username=username, password=hashed_password, email=email)
    else:
        user = User(username=username, password=hashed_password, email=email, user_type=role)

    db.session.add(user)
    db.session.commit()
    return user


# Controller function to log in a user
def login_user(username, password):
    user = User.query.filter_by(username=username).first()  # Find user by username
    if user and check_password_hash(user.password, password):  # Check password
        return f"User {username} logged in successfully!"
    else:
        return "Invalid username or password."

# Controller function to accept or reject an application [EMPLOYER]
def review_application(application_id, is_accepted):
    application = Application.query.get(application_id)
    if not application:
        return f"Application with ID {application_id} does not exist."
    
    application.is_accepted = is_accepted
    db.session.commit()
    
    status = 'accepted' if is_accepted else 'rejected'
    return f'Application {application_id} has been {status}.'

# Controller function for job seekers to view their accepted applications [JOB_SEEKER]
def view_job_status(job_seeker_id):
    job_seeker = JobSeeker.query.get(job_seeker_id)
    if not job_seeker:
        return f"Job Seeker with ID {job_seeker_id} does not exist."

    # Get all applications and their statuses for the job seeker
    applications_status = []
    
    for app in job_seeker.applications:
        status = "Pending"
        if app.is_accepted is True:
            status = "Accepted"
        elif app.is_accepted is False:
            status = "Rejected"

        # Collect job details with the status
        applications_status.append({
            "job_id": app.job_id,
            "job_category": app.job.category,
            "description": app.job.description,
            "status": status
        })

    return applications_status


# Controller function to create a job advertisement [EMPLOYER]
def create_job(category, description, employer_id):
    employer = Employer.query.get(employer_id)
    if not employer:
        return f"Employer with ID {employer_id} does not exist. Job not created."

    job = Job(category=category, description=description, employer_id=employer_id)
    db.session.add(job)
    db.session.commit()
    return f"Job '{category}' created successfully under Employer ID {employer_id}."

# Controller function for job seekers to apply to a job [JOB_SEEKER]
def apply_to_job(job_id, job_seeker_id, application_text):
    application = Application(job_id=job_id, job_seeker_id=job_seeker_id, application_text=application_text)
    db.session.add(application)
    db.session.commit()

# Controller function to retrieve applicants for a specific job [EMPLOYER]
def get_applicants_for_job(job_id):
    job = Job.query.get_or_404(job_id)
    return job.applications

# Controller function to initialize the database [ADMIN]
def initialize():
    db.create_all()
