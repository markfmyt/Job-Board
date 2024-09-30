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

<details>
<summary>Getting Started (Click to expand)</summary>

Here's a step-by-step guide to get you started with the Job Application System:

1. Sign up a job seeker:
   ```
   flask user signup bob bobpass1 bob@mail.com job_seeker
   ```

2. Sign up an employer:
   ```
   flask user signup amazon jungle12 amazon@mail.com employer
   ```

3. View all users (as admin):
   ```
   flask admin print_all
   ```

4. Create a job listing (as employer):
   ```
   flask employer create_job "Software Engineer" "Looking for backend developers with React experience" 2
   ```
   Note: The number 2 at the end represents the employer's user ID.

5. Apply for the job (as job seeker):
   ```
   flask job apply 1 1 "Hello, I have 10 years of React experience"
   ```
   Note: The first 1 is the job ID, and the second 1 is the job seeker's user ID.

6. View applicants for the job (as employer):
   ```
   flask employer view_applicants 1
   ```
   Note: The 1 represents the job ID.

7. Review and accept the application (as employer):
   ```
   flask employer review 1 accept
   ```
   Note: The 1 represents the application ID.

8. View job application status for all applications for a particular job seeker:
   ```
   flask job status 1
   ```
   Note: The 1 represents the job seeker's user ID.

This walkthrough demonstrates the basic flow of the application, from user creation to job application and review.

</details>

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

- View job application status for all applications for a particular job seeker:
  ```
  flask job status <job_seeker_id>
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
