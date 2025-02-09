

# Job Board

![Django Logo](https://www.djangoproject.com/m/img/logos/django-logo-positive.png)

## Overview

**Job Board** is a web application built using the Django framework. It serves as a platform for connecting job seekers and companies, facilitating job postings, applications, and technical content sharing.

## Key Features

- **Authentication System:** Allows users to register either as employees or companies.
- **Job Posting:** Companies can post job vacancies.
- **Job Application:** Employees can apply for jobs, and their information is sent to the company via email.
- **Technical Posts:** Employees can share technical posts.
- **Interactive Features:** Includes a comment system, likes, and reply functionality for posts.
- **Email Verification:** Users can verify their email addresses to activate their accounts.

---

## Technologies Used

- **Framework:** Django
- **Database:** SQLite (default), but can be configured for other databases.
- **Frontend:** HTML, CSS, JavaScript
- **Email Backend:** SMTP for sending emails.

---

## How to Run the Project

### Prerequisites

1. **Python:** Ensure Python is installed on your machine. You can download it from [python.org](https://www.python.org/).
2. **pip:** Python's package manager.
3. **Git:** To clone the project from GitHub.

### Steps

#### 1. Clone the Project

```bash
git clone https://github.com/your-username/Job-board.git
cd Job-board
```

#### 2. Create a Virtual Environment

```bash
python -m venv venv
source venv/bin/activate  # For Linux/Mac
venv\Scripts\activate     # For Windows
```

#### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

#### 4. Apply Database Migrations

```bash
python manage.py migrate
```

#### 5. Create a Superuser

```bash
python manage.py createsuperuser
```

#### 6. Run the Local Server

```bash
python manage.py runserver
```

After running the server, you can access the application by navigating to:

```
http://127.0.0.1:8000/
```

---

## How to Use the Project

1. **Sign Up/Login:**
   - Register as a new user (either as an employee or a company).
   - Verify your email to activate your account.

2. **Post a Job (For Companies):**
   - Log in as a company.
   - Go to the "Post a Job" page and add the job details.

3. **Apply for a Job (For Employees):**
   - Log in as an employee.
   - Search for suitable jobs and submit your application.

4. **Manage Content:**
   - Use the admin panel (`/admin`) to manage users, jobs, and posts.


