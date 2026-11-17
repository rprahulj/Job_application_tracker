# Job Application Tracker API

## About the Project

Job Application Tracker is a REST API developed using Python, Django, and Django REST Framework.

This project helps users manage their job applications in one place. Users can add job applications, track their application status, manage interviews, write notes, and set reminders.

The API uses JWT authentication to secure user accounts and ensure that users can access only their own data.

## Technologies Used

- Python
- Django
- Django REST Framework
- SQLite
- Django ORM
- JWT Authentication

## Features

- User registration and login.
- Secure authentication using JWT tokens.
- Add, view, update, and delete job applications.
- Manage interview details and schedules.
- Add and manage notes for each application.
- Create reminders for important activities.
- Send email reminders automatically.
- View application statistics.
- Filter applications by status and company.
- Search applications by company, role, location, and description.
- Sort application records.
- Pagination for application lists.
- Secure data access for individual users.

## Project Structure

```text
job_application_tracker/
│
├── job_application_tracker/
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   └── wsgi.py
│
├── applications/
│   ├── management/
│   │   └── commands/
│   │       └── send_due_reminders.py
│   ├── models.py
│   ├── serializers.py
│   ├── permissions.py
│   ├── views.py
│   ├── admin.py
│   └── tests.py
│
├── manage.py
├── requirements.txt
├── README.md
└── .gitignore
```

## Database Models

The project uses four main database models.

### 1. Application

Stores information about job applications.

- Company name
- Job role
- Location
- Job description
- Job URL
- Application status
- Application date

### 2. Interview

Stores interview-related information.

- Interview date and time
- Interview type
- Interviewer name
- Meeting link
- Interview result

### 3. Note

Stores personal notes related to job applications.

- Note content
- Created date
- Updated date

### 4. Reminder

Stores reminder information.

- Reminder date and time
- Reminder message
- Email sent status

### Database Relationships

- One user can have multiple job applications.
- One application can have multiple interviews.
- One application can have multiple notes.
- One application can have multiple reminders.

## API Endpoints

The project contains 28 functional API operations.

### Authentication APIs

| Method | Endpoint | Description |
|---|---|---|
| POST | `/api/register/` | Register a new user |
| POST | `/api/token/` | Login and get JWT tokens |
| POST | `/api/token/refresh/` | Refresh access token |

### Application APIs

| Method | Endpoint | Description |
|---|---|---|
| GET | `/api/applications/` | Get all applications |
| POST | `/api/applications/` | Add a new application |
| GET | `/api/applications/{id}/` | Get application details |
| PUT | `/api/applications/{id}/` | Update an application |
| PATCH | `/api/applications/{id}/` | Update selected fields |
| DELETE | `/api/applications/{id}/` | Delete an application |

### Interview APIs

| Method | Endpoint | Description |
|---|---|---|
| GET | `/api/interviews/` | Get all interviews |
| POST | `/api/interviews/` | Add an interview |
| GET | `/api/interviews/{id}/` | Get interview details |
| PUT | `/api/interviews/{id}/` | Update an interview |
| PATCH | `/api/interviews/{id}/` | Update selected fields |
| DELETE | `/api/interviews/{id}/` | Delete an interview |

### Notes APIs

| Method | Endpoint | Description |
|---|---|---|
| GET | `/api/notes/` | Get all notes |
| POST | `/api/notes/` | Add a new note |
| GET | `/api/notes/{id}/` | Get note details |
| PUT | `/api/notes/{id}/` | Update a note |
| PATCH | `/api/notes/{id}/` | Update selected fields |
| DELETE | `/api/notes/{id}/` | Delete a note |

### Reminder APIs

| Method | Endpoint | Description |
|---|---|---|
| GET | `/api/reminders/` | Get all reminders |
| POST | `/api/reminders/` | Add a reminder |
| GET | `/api/reminders/{id}/` | Get reminder details |
| PUT | `/api/reminders/{id}/` | Update a reminder |
| PATCH | `/api/reminders/{id}/` | Update selected fields |
| DELETE | `/api/reminders/{id}/` | Delete a reminder |

### Statistics API

| Method | Endpoint | Description |
|---|---|---|
| GET | `/api/stats/` | Get application statistics |

## User Authentication and Data Security

The project uses JWT authentication to protect API endpoints.

The authentication process works as follows:

1. A user registers an account.
2. The user logs in with a username and password.
3. The server generates access and refresh tokens.
4. The user sends the access token with API requests.
5. The server verifies the token before allowing access.

### How User Data Is Protected

- Every user's application list is filtered using the logged-in user.
- The server assigns record ownership automatically.
- Users cannot access another user's applications.
- Interview, note, and reminder records are checked against application ownership.
- Users cannot create related records using another user's application ID.

This ensures that each user can access only their own information.

## Search, Filtering and Sorting

The application list supports searching, filtering, and sorting.

Example request:

```text
/api/applications/?status=interview&company=Google&search=python&ordering=-applied_at&page=1
```

Available options:

- Status: Filter applications by status.
- Company: Search by company name.
- Search: Search by role, company, location, or description.
- Ordering: Sort applications by date, company, or update time.
- Page: Get a particular page of results.

## Application Statistics

The statistics API provides information about job applications.

It includes:

- Total number of applications.
- Number of applications in each status.
- Number of applications submitted each week.

The project uses Django ORM functions such as `Count()`, `values()`, `annotate()`, and `TruncWeek()` to calculate statistics directly in the database.

## Automated Email Reminders

The project includes a Django management command to send reminder emails.

Command:

```bash
python manage.py send_due_reminders
```

How it works:

1. The command finds reminders whose scheduled time has passed.
2. It checks whether the reminder has already been sent.
3. It sends an email to the user.
4. It updates the sent date after successful email delivery.

The command can be scheduled to run automatically using Cron or Windows Task Scheduler.

## Installation and Setup

Follow these steps to run the project on your computer.

### Step 1: Clone the Repository

```bash
git clone https://github.com/YOUR_USERNAME/job-application-tracker.git
```

### Step 2: Open the Project Folder

```bash
cd job-application-tracker
```

### Step 3: Create a Virtual Environment

```bash
python -m venv venv
```

Activate the environment.

For Windows:

```bash
venv\Scripts\activate
```

For Linux or macOS:

```bash
source venv/bin/activate
```

### Step 4: Install Required Packages

```bash
pip install -r requirements.txt
```

### Step 5: Create Database Tables

```bash
python manage.py makemigrations
python manage.py migrate
```

### Step 6: Create Admin Account

```bash
python manage.py createsuperuser
```

### Step 7: Run the Development Server

```bash
python manage.py runserver
```

The project will be available at:

```text
http://127.0.0.1:8000/
```

## Testing

To run the available test cases:

```bash
python manage.py test
```

The included tests check user data isolation and prevent users from accessing applications owned by other users.
