# Job Application System

This is a Flask-based Job Application System that allows users to sign up, create job listings, apply for jobs, and manage applications. The system supports three types of users: Job Seekers, Employers, and Admins.

## Features

- User authentication (signup and login)
- Job listing creation and management
- Job application submission and review
- Role-based access control (Admin, Employer, Job Seeker)

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/markfmyt/Job-Board
   ```

2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Initialize the database:
   ```
   flask init
   ```

## Usage

The application provides a CLI interface for various operations. Here are the available commands:

### User Commands

- Signup a new user:
  ```
  flask user signup <username> <password> <email> <role>
  ```
  Role must be one of: 'admin', 'employer', or 'job_seeker'

- List all users:
  ```
  flask user list_all
  ```

- List all job postings:
  ```
  flask user job_list
  ```

### Job Seeker Commands

- View accepted job offers for a job seeker:
  ```
  flask job offers <job_seeker_id>
  ```

- Apply to a job:
  ```
  flask job apply <job_id> <job_seeker_id> <application_text>
  ```

### Employer Commands

- Review a job application:
  ```
  flask employer review <application_id> <decision>
  ```
  Decision must be either 'accept' or 'reject'

- Create a new job listing:
  ```
  flask employer create_job <category> <description> <employer_id>
  ```

- View applicants for a specific job:
  ```
  flask employer view_applicants <job_id>
  ```

### Admin Commands

- Print all entities in the database:
  ```
  flask admin print_all
  ```

- Drop all tables in the database:
  ```
  flask admin drop_all
  ```

## Database Schema

The application uses SQLAlchemy with the following main models:
- User (base class for Admin, Employer, and JobSeeker)
- Job
- Application

