import click
from flask import Flask
from flask.cli import AppGroup
from flask_sqlalchemy import SQLAlchemy
from App.database import db, init_db, get_migrate
from App import User, Admin, Employer, JobSeeker, Job, Application
from App import (get_all_users, get_all_jobs, get_all_entities, drop_database, remove_application, remove_job, remove_user, create_user, login_user, review_application, view_job_status_all, view_job_status, create_job, apply_to_job, get_applicants_for_job, initialize)
from App.main import create_app

app = create_app()
migrate = get_migrate(app)

# CLI command to initialize the database
# Usage: flask init
@app.cli.command("init", help="Creates and initializes the database")
def init_db_command():
    initialize()
    print('Database initialized.')

'''
User Commands
'''
user_cli = AppGroup('user', help='User object commands')

# Usage: flask user signup <username> <password> <email> <role>
@user_cli.command("signup", help="Signup a user")
@click.argument("username")
@click.argument("password")
@click.argument("email")
@click.argument("role")
def signup_user_command(username, password, email, role):
    if role not in ['admin', 'employer', 'job_seeker']:
        print("Invalid role. Choose from 'admin', 'employer', or 'job_seeker'.")
        return
    user = create_user(username, password, email, role)
    print(f'User {username} signed up as {role}!')

# Usage: flask user list_all
@user_cli.command("list_all", help="Lists users in the database")
def list_users_command():
    output = get_all_users()
    print(output)

# Usage: flask user job_list // View Jobs [ALL USERS]
@user_cli.command("job_list", help="List all job postings")
def list_jobs_command():
    output = get_all_jobs()
    print(output)


app.cli.add_command(user_cli)

'''
Job Commands
'''
job_cli = AppGroup('job', help='Job object commands')
# Usage:  flask job application_all <job_seeker_id> // View Accepted Jobs [JOB_SEEKER]
@job_cli.command("application_all", help="View job applications")
@click.argument("job_seeker_id")
def view_job_status_all_command(job_seeker_id):
    applications = view_job_status_all(job_seeker_id)
    if applications:
        for application in applications:
            print(f"Job ID: {application['job_id']}, Category: {application['job_category']}, Description: {application['description']}, Status: {application['status']}")
    else:
        print(f"No applications found for Job Seeker {job_seeker_id}.")

# Usage:  flask job status <job_seeker_id> <application_id>// View Application Status [JOB_SEEKER]
@job_cli.command("status", help="View job applications")
@click.argument("job_seeker_id")
@click.argument("application_id")
def view_job_status_command(job_seeker_id, application_id):
    result = view_job_status(job_seeker_id,application_id)
    print(result)



# Usage: flask job apply <job_id> <job_seeker_id> <application_text> // Apply to Job [JOB_SEEKER]
@job_cli.command("apply", help="Apply to a job")
@click.argument("job_id")
@click.argument("job_seeker_id")
@click.argument("application_text")
def apply_command(job_id, job_seeker_id, application_text):
    apply_to_job(job_id, job_seeker_id, application_text)
    print(f'Job Seeker {job_seeker_id} applied to Job ID {job_id}.')

app.cli.add_command(job_cli)

'''
Employer Commands
'''
employer_cli = AppGroup('employer', help='Admin commands')
# Usage: flask employer review <application_id> <decision> // Review Applicants [EMPLOYERS]
@employer_cli.command("review", help="Review a job application (accept/reject)")
@click.argument("application_id")
@click.argument("decision")  # 'accept' or 'reject'
def review_application_command(application_id, decision):
    if decision.lower() == 'accept':
        result = review_application(application_id, True)
    elif decision.lower() == 'reject':
        result = review_application(application_id, False)
    else:
        result = "Invalid decision. Use 'accept' or 'reject'."
    
    print(result)

# Usage: flask employer create_job <category> <description> <employer_id> // Create Job Advertisement [EMPLOYERS]
@employer_cli.command("create_job", help="Create a job")
@click.argument("category")
@click.argument("description")
@click.argument("employer_id")
def create_job_command(category, description, employer_id):
    result = create_job(category, description, employer_id)
    print(result)

# Usage: flask employer view_applicants <job_id> // View Applicants [EMPLOYER]
@employer_cli.command("view_applicants", help="List all applicants for a specific job")
@click.argument("job_id")
def get_applicants_for_job_command(job_id):
    # Call the controller function to get the applicants for the job
    applications = get_applicants_for_job(job_id)
    
    # Display the applicants
    if applications:
        for application in applications:
            print(f"Application ID: {application.application_id}, Job Seeker ID: {application.job_seeker_id}, Status: {'Accepted' if application.is_accepted else 'Rejected' if application.is_accepted is False else 'Pending'}")
    else:
        print(f"No applicants for Job ID {job_id}.")

app.cli.add_command(employer_cli)

'''
Admin Commands
'''
admin_cli = AppGroup('admin', help='Admin commands')
# Usage: flask admin print_all 
@admin_cli.command("print_all", help="Print all entities in the database")
def print_all_entities_command():
    output = get_all_entities()
    print(output)

# Usage: flask admin drop_all <admin_id>
@admin_cli.command("drop_all", help="Drop all tables in the database")
@click.argument('admin_id')
def drop_all_command(admin_id):
    print(drop_database(admin_id))

# Usage: flask admin remove_user <user_id>
@admin_cli.command('remove_user', help="Remove a user by ID")
@click.argument('user_id')
def remove_user_command(user_id):
    result = remove_user(user_id)
    print(result)

# Usage: flask admin remove_job <job_id>
@admin_cli.command('remove_job', help="Remove a job by ID")
@click.argument('job_id')
def remove_job_command(job_id):
    result = remove_job(job_id)
    print(result)

# Usage: flask admin remove_application <application_id>
@admin_cli.command('remove_application', help="Remove an application by ID")
@click.argument('application_id')
def remove_application_command(application_id):
    result = remove_application(application_id)
    print(result)
app.cli.add_command(admin_cli)


if __name__ == "__main__":
    app.run()
