# Job Application Tracker API

A RESTful backend application built using **Python, Django, Django REST Framework, SQLite, and JWT Authentication** to help users manage their job applications, interviews, notes, and reminders in one place.

The project focuses on secure API development, user-level data isolation, database optimisation, and automated email reminders.

## 🚀 Features

- **JWT Authentication:** Secure user registration, login, and token refresh.
- **Job Application Management:** Create, retrieve, update, and delete job applications.
- **Interview Management:** Schedule interviews and maintain interview details.
- **Notes Management:** Maintain notes associated with job applications.
- **Email Reminders:** Schedule reminders and send automated email notifications.
- **Statistics Dashboard:** View application statistics grouped by status and week.
- **Filtering:** Filter applications by status and company.
- **Full-Text Search:** Search applications by company, role, location, and description.
- **Sorting:** Sort records by application date, company, and update date.
- **Pagination:** Paginate API responses to handle larger datasets.
- **Data Isolation:** Ensure users can access only their own records.
- **Database Optimisation:** Use composite indexes and database-level aggregation.

## 🛠️ Technology Stack

| Technology | Purpose |
|---|---|
| Python | Programming language |
| Django | Backend framework |
| Django REST Framework | REST API development |
| SQLite | Relational database |
| Django ORM | Database operations |
| Simple JWT | Authentication |
| Django Management Commands | Scheduled email reminders |

## 🏗️ Project Architecture

```text
Client (Postman / Frontend)
          |
          v
    REST API Routes
          |
          v
   JWT Authentication
          |
          v
 Django REST Framework
          |
          v
   Views & Serializers
          |
          v
       Django ORM
          |
          v
      SQLite Database
```

## 📁 Project Structure

```text
job_application_tracker/
│
├── tracker/
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   └── wsgi.py
│
├── applications/
│   ├── management/
│   │   └── commands/
│   │       └── send_due_reminders.py
│   ├── migrations/
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

## 🗄️ Database Design

The application uses four main domain models.

### 1. Application
Stores job application information.

- Company name
- Job role
- Location
- Job description
- Job URL
- Application status
- Application date
- Created and updated timestamps

### 2. Interview
Stores interview information associated with an application.

- Interview date and time
- Interview type
- Interviewer
- Meeting link or location
- Interview outcome

### 3. Note
Stores personal notes associated with an application.

- Note content
- Created timestamp
- Updated timestamp

### 4. Reminder
Stores reminder information.

- Reminder date and time
- Reminder message
- Email delivery timestamp

### Database Relationships

```text
User
 |
 | 1-to-Many
 |
Application
 |
 |------ Interview (1-to-Many)
 |
 |------ Note (1-to-Many)
 |
 |------ Reminder (1-to-Many)
```

Each application belongs to one user. Interviews, notes, and reminders belong to an application.

## 🔐 Authentication and Security

The API uses JSON Web Token (JWT) authentication through `djangorestframework-simplejwt`.

### Authentication Flow

1. User registers an account.
2. User logs in using username and password.
3. Server generates access and refresh tokens.
4. Client sends the access token with protected API requests.
5. Server validates the token and identifies the authenticated user.

Example authorisation header:

```http
Authorisation: Bearer <access_token>
```

### Per-User Data Isolation

Data isolation is implemented at the backend level.

- Every application queryset is filtered using `request.user`.
- Ownership is assigned using the authenticated user, not a user ID supplied in the request body.
- Related-object IDs are validated against the logged-in user's applications.
- Users cannot retrieve or modify another user's records through manipulated IDs.

This protects the application against insecure direct object reference (IDOR) vulnerabilities.

## 📡 API Documentation

The project provides **28 functional HTTP operations across 12 URL patterns**, excluding the automatically generated API root.

### Authentication APIs

| Method | Endpoint | Description |
|---|---|---|
| POST | `/api/register/` | Register a new user |
| POST | `/api/token/` | Login and obtain JWT tokens |
| POST | `/api/token/refresh/` | Refresh access token |

### Application APIs

| Method | Endpoint | Description |
|---|---|---|
| GET | `/api/applications/` | List applications |
| POST | `/api/applications/` | Create application |
| GET | `/api/applications/{id}/` | Retrieve application |
| PUT | `/api/applications/{id}/` | Replace application |
| PATCH | `/api/applications/{id}/` | Partially update application |
| DELETE | `/api/applications/{id}/` | Delete application |

### Interview APIs

| Method | Endpoint | Description |
|---|---|---|
| GET | `/api/interviews/` | List interviews |
| POST | `/api/interviews/` | Create interview |
| GET | `/api/interviews/{id}/` | Retrieve interview |
| PUT | `/api/interviews/{id}/` | Replace interview |
| PATCH | `/api/interviews/{id}/` | Partially update interview |
| DELETE | `/api/interviews/{id}/` | Delete interview |

### Notes APIs

| Method | Endpoint | Description |
|---|---|---|
| GET | `/api/notes/` | List notes |
| POST | `/api/notes/` | Create note |
| GET | `/api/notes/{id}/` | Retrieve note |
| PUT | `/api/notes/{id}/` | Replace note |
| PATCH | `/api/notes/{id}/` | Partially update note |
| DELETE | `/api/notes/{id}/` | Delete note |

### Reminder APIs

| Method | Endpoint | Description |
|---|---|---|
| GET | `/api/reminders/` | List reminders |
| POST | `/api/reminders/` | Create reminder |
| GET | `/api/reminders/{id}/` | Retrieve reminder |
| PUT | `/api/reminders/{id}/` | Replace reminder |
| PATCH | `/api/reminders/{id}/` | Partially update reminder |
| DELETE | `/api/reminders/{id}/` | Delete reminder |

### Statistics API

| Method | Endpoint | Description |
|---|---|---|
| GET | `/api/stats/` | Retrieve application statistics |

## 🔎 Filtering, Searching and Pagination

Application listing supports multiple query parameters.

Example:

```http
GET /api/applications/?status=interview&company=Google&search=python&ordering=-applied_at&page=1
```

Supported parameters:

| Parameter | Description |
|---|---|
| `status` | Filter by application status |
| `company` | Filter by company name |
| `search` | Search across configured text fields |
| `ordering` | Sort results |
| `page` | Select pagination page |

## 📊 Statistics and Database Aggregation

The statistics endpoint provides:

- Total number of applications.
- Application counts grouped by status.
- Weekly application counts.

Django ORM aggregation is used to perform calculations at the database level.

Important ORM functions:

- `Count()` – Count database records.
- `values()` – Group records by selected fields.
- `annotate()` – Calculate aggregated values.
- `TruncWeek()` – Group dates by week.

## 📧 Automated Email Reminders

The project includes a custom Django management command:

```bash
python manage.py send_due_reminders
```

The command:

1. Finds reminders whose due date has passed.
2. Skips reminders already marked as sent.
3. Sends an email to the application owner's email address.
4. Updates the `sent_at` field after successful email delivery.

For automatic execution, schedule this command using:

- Linux Cron
- Windows Task Scheduler

The implementation prevents repeated sends during normal sequential runs. Production-grade exactly-once delivery requires additional handling, such as a transactional outbox and an idempotent email provider.

## ⚙️ Installation and Setup

### 1. Clone the Repository

```bash
git clone https://github.com/YOUR_USERNAME/job-application-tracker.git
```

```bash
cd job-application-tracker
```

### 2. Create a Virtual Environment

```bash
python -m venv venv
```

Activate it:

**Windows**

```bash
venv\Scripts\activate
```

**Linux / macOS**

```bash
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Apply Database Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### 5. Create a Superuser

```bash
python manage.py createsuperuser
```

### 6. Start Development Server

```bash
python manage.py runserver
```

The API will be available at:

```text
http://127.0.0.1:8000/
```

## 🧪 Testing

Run the test suite:

```bash
python manage.py test
```

The included tests cover important ownership scenarios, including:

- Listing only the authenticated user's applications.
- Preventing access to another user's application.
- Preventing creation of related records against another user's application.

Additional CRUD, authentication, and concurrent reminder tests can be added as the project evolves.



---

⭐ If you find this project useful, consider giving it a star!
