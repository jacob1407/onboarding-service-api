# Employee Onboarding API

## Overview

This application automates the employee onboarding process by streamlining application provisioning and access management. The system manages the end-to-end workflow of granting new employees access to the necessary applications and systems based on their assigned roles within an organization.

### Key Features

- **Role-based Application Provisioning**: Automatically determines which applications a new employee needs access to based on their assigned role
- **Automated Email Workflow**: Sends provisioning requests to application owners/contacts when onboarding begins
- **Multi-tenant Organization Support**: Manages users and applications across multiple organizations
- **Onboarding Status Tracking**: Tracks the progress of each employee's onboarding process (pending, in progress, complete, cancelled)
- **Request Management**: Handles approval/denial workflows for application access requests
- **Authentication & Authorization**: JWT-based authentication with role-based access control

### How It Works

1. **Employee Setup**: New employees are added to the system with their role and organization
2. **Onboarding Initiation**: Admins start the onboarding process for an employee
3. **Application Discovery**: The system identifies all applications required for the employee's role
4. **Request Distribution**: Automated emails are sent to application contacts requesting access provisioning
5. **Tracking & Confirmation**: The system tracks responses and updates onboarding status as applications are provisioned

## Tech Stack

### Backend Framework
- **FastAPI**: Modern, fast web framework for building APIs with Python
- **Python 3.11+**: Core programming language
- **Uvicorn**: ASGI server for running the FastAPI application

### Database & ORM
- **PostgreSQL**: Primary database for data persistence
- **SQLAlchemy 2.0**: Modern Python SQL toolkit and Object-Relational Mapping (ORM)
- **Alembic**: Database migration tool for SQLAlchemy

### Authentication & Security
- **python-jose**: JWT token handling for authentication
- **passlib**: Password hashing and verification
- **OAuth 2.0**: Authentication flow implementation

### Email Services
- **Resend**: Email service provider
- **HTTPX**: HTTP client for external API communication

### Development & Deployment
- **Docker**: Containerization for development and deployment
- **Docker Compose**: Multi-container orchestration
- **Alembic**: Database schema versioning and migrations

### Development Tools
- **Pydantic**: Data validation and settings management
- **SQLAlchemy Models**: Type-safe database schema definitions
- **FastAPI Dependency Injection**: Clean separation of concerns

## API Overview

### Main Endpoints

- **Authentication** (`/auth`): Login, token management
- **Users** (`/users`): User management and registration
- **Roles** (`/roles`): Role definition and management
- **Applications** (`/applications`): Application catalog management
- **Onboarding** (`/onboarding`): Core onboarding workflow
- **Contacts** (`/contacts`): Application contact management
- **Health** (`/health`): Service health monitoring

### Core Workflows

1. **Start Onboarding**: `POST /onboarding/start` - Initiates the onboarding process
2. **Confirm Requests**: `GET /onboarding/requests/{id}/confirm` - Handle application access confirmations
3. **Manage Applications**: CRUD operations for applications and their associated roles
4. **User Management**: Create and manage employees within organizations

## Project Structure

```
src/
├── models/          # SQLAlchemy database models
├── routers/         # FastAPI route handlers
├── services/        # Business logic layer
├── data_access/     # Database access layer
├── schemas/         # Pydantic models for API validation
├── enums/          # Application enums and constants
└── db/             # Database configuration and connection
```

## Development Setup

### Prerequisites
- Python 3.11+
- Docker and Docker Compose
- PostgreSQL (if running locally)

### Using Virtual Environment

```bash
# Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Note: On macOS, you may need to install PostgreSQL
brew install postgresql
```

### Using Docker (Recommended)

```bash
# Build and start all services
docker compose up --build

# The API will be available at http://localhost:8080
```

### Individual Docker Commands

```bash
# Build the image
docker build -t onboarding-service-api .

# Run the container
docker run -p 8080:8080 onboarding-service-api
```

## Database Management

### Database Access

```bash
# Connect to the database in the Docker container
docker exec -it onboarding-db psql -U myuser -d onboarding

# List all tables
\dt

# Exit the database
\q
```

### Database Migrations

```bash
# Create a new migration
alembic revision --autogenerate -m "description of changes"

# Apply migrations
alembic upgrade head

# View migration history
alembic history
```

## Environment Configuration

The application uses environment variables for configuration. Key variables include:

- `DB_URL`: Database connection string
- Email service credentials (Resend/SendGrid API keys)
- JWT secret keys
- CORS origins for frontend integration
