from App.models import db, User, Admin, Employer, JobSeeker, Job, Application
from werkzeug.security import generate_password_hash, check_password_hash

# Controller functions

# Controller function to create a user with specified role [ALL USERS]
def create_user(username, password, email, role):
    # Check for unique username
    existing_user_by_username = User.query.filter_by(username=username).first()
    if existing_user_by_username:
        return f"Username '{username}' is already taken. Please choose a different username."
    
    # Check for unique email
    existing_user_by_email = User.query.filter_by(email=email).first()
    if existing_user_by_email:
        return f"Email '{email}' is already registered. Please use a different email address."

    # Validate role
    if role not in ['admin', 'employer', 'job_seeker']:
        return f"Invalid role '{role}'. Choose from 'admin', 'employer', or 'job_seeker'."

    hashed_password = generate_password_hash(password)

    # Create the user based on the role
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
    # Check if the job exists
    job = Job.query.get(job_id)
    if not job:
        return f"Job with ID {job_id} does not exist."

    # Check if the job seeker exists
    job_seeker = JobSeeker.query.get(job_seeker_id)
    if not job_seeker:
        return f"Job Seeker with ID {job_seeker_id} does not exist."

    # Check for duplicate applications
    existing_application = Application.query.filter_by(job_id=job_id, job_seeker_id=job_seeker_id).first()
    if existing_application:
        return f"Job Seeker {job_seeker_id} has already applied for Job {job_id}."

    # Create the application if all validations pass
    application = Application(job_id=job_id, job_seeker_id=job_seeker_id, application_text=application_text)
    db.session.add(application)
    db.session.commit()
    return f"Application submitted for Job {job_id} by Job Seeker {job_seeker_id}."


# Controller function to retrieve applicants for a specific job [EMPLOYER]
def get_applicants_for_job(job_id):
    job = Job.query.get_or_404(job_id)
    return job.applications

# Controller function for removing a user [ADMIN]
def remove_user(user_id):
    user = User.query.get(user_id)
    if not user:
        return f"User with ID {user_id} does not exist."
    
    db.session.delete(user)
    db.session.commit()
    return f"User with ID {user_id} removed successfully."

# Controller function for removing a job [ADMIN]
def remove_job(job_id):
    job = Job.query.get(job_id)
    if not job:
        return f"Job with ID {job_id} does not exist."
    
    db.session.delete(job)
    db.session.commit()
    return f"Job with ID {job_id} removed successfully."

# Controller function for removing an application [ADMIN]
def remove_application(application_id):
    application = Application.query.get(application_id)
    if not application:
        return f"Application with ID {application_id} does not exist."
    
    db.session.delete(application)
    db.session.commit()
    return f"Application with ID {application_id} removed successfully."

# Controller function to initialize the database [ADMIN]
def initialize():
    db.create_all()
