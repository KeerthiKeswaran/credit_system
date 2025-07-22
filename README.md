# Credit Approval System Backend
### (Backend Assignment - Alemeno)

This project is a credit evaluation and loan management system built using Django REST Framework. It enables customer onboarding, credit approval, loan issuance, loan eligibility analysis, and EMI tracking. It also includes a background task pipeline using Celery and Redis for initial data loading.

The project is containerized using Docker and can be deployed seamlessly using Docker Compose, making it platform-independent and production-friendly.

---

## Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/KeerthiKeswaran/credit_system.git
cd credit_system
```

2. Environment Configuration
Create a .env file in the root directory. You may specify environment-specific variables like database configuration or secret keys. In this project, most settings are Django defaults for development.

Ensure .env is added to .gitignore to avoid committing secrets.

3. Docker Setup (Recommended for Deployment)
The entire application is containerized and configured via Docker Compose.

To build and start the services:

```bash
docker-compose up --build
```

This will start:

Django web server via Gunicorn

Redis (for Celery message broker)

Celery worker for async tasks

The app will be accessible at: http://127.0.0.1:8000/

4. Django Setup (Without Docker - Development Only)
If you prefer to run the app locally without Docker:

```bash
# Install Python dependencies
pip install -r requirements.txt

# Run migrations
python manage.py migrate

# Start the server
python manage.py runserver
```

Folder Structure
```bash
credit_system/
│
├── credit_app/             # Django app for handling logic
│   ├── models.py           # Customer and Loan models
│   ├── views.py            # All APIs (Register, Check Eligibility, etc.)
│   ├── tasks.py            # Celery task to load Excel data
│   ├── serializers.py      # DRF serializers for input/output validation
│   ├── urls.py             # App-level URL routing
│
├── credit_system/          # Django project config
│   ├── settings.py         # Django settings
│   ├── urls.py             # Project URL routing
│   ├── wsgi.py             # Gunicorn entry point
│ 
├── tests_scripts/          # Contains the test scripts seperately for each api endpoints
│   ├── test_register.py        
│   ├── test_eligibility.py             
│   ├── test_create_loan.py    
│   ├── test_view_loans.py        
│   ├── test_loan_update.py             
│   ├── test_summary.py  
│
├── docker-compose.yml      # Docker Compose services
├── Dockerfile              # Web image build
├── requirements.txt        # Python dependencies
├── manage.py               # Django CLI entry
├── .env                    # Environment variables (not tracked)
└── README.md               # Project documentation
```

### API Endpoints

1. Register Customer
Endpoint: POST /api/register/

Payload:
```bash
{
  "first_name": "Keerthi",
  "last_name": "Keswaran",
  "age": 22,
  "monthly_income": 50000,
  "phone_number": "9876543210"
}
```

Response:
```bash
{
  "id": 1,
  "name": "Keerthi Keswaran",
  "age": 22,
  "monthly_income": 50000.0,
  "approved_limit": 1800000.0,
  "phone_number": "9876543210"
}
```

2. Check Loan Eligibility
Endpoint: POST /api/check-eligibility/

Payload:
```bash
{
  "customer_id": 1,
  "loan_amount": 100000,
  "interest_rate": 10,
  "tenure": 12
}
```

Response:

```bash
{
  "customer_id": 1,
  "approval": true,
  "interest_rate": 10.0,
  "tenure": 12,
  "monthly_installment": 8791.59,
  "message": "Eligible for the requested loan"
}
```

Eligibility logic is based on current debt, EMI-to-income ratio, and past behavior.

3. Create Loan
Endpoint: POST /api/create-loan/

Payload:
```bash
{
  "customer_id": 1,
  "loan_amount": 100000,
  "interest_rate": 10,
  "tenure": 12
}
```

Response:
```bash
{
  "id": 1,
  "loan_amount": 100000.0,
  "tenure": 12,
  "interest_rate": 10.0,
  "monthly_installment": 8791.59,
  "emis_paid_on_time": 0,
  "start_date": "2025-07-23",
  "end_date": "2026-07-23",
  "customer": 1
}
```

4. Update EMI Status
Endpoint: POST /api/update-loan/<loan_id>/

Payload:
```bash
{
  "emis_paid": 6
}
```

Response:
```bash
{
  "message": "Loan 1 updated successfully with 6 EMIs paid"
}
```

5. Retrieve Customer Loans
   
Endpoint: GET /api/loans/<customer_id>/

Response: List of all loans taken by the customer.

Celery & Redis (Async Task System)
A Celery worker is connected via Redis.

load_initial_data() task automatically reads customer_data.xlsx and loan_data.xlsx and populates the database.

To manually trigger the task:

```bash
celery -A credit_system worker --loglevel=info
```

Docker Services
Your docker-compose.yml includes:

```bash
services:
  web:
    build: .
    command: gunicorn credit_system.wsgi:application --bind 0.0.0.0:8000
    ports:
      - "8000:8000"
    depends_on:
      - redis
    env_file:
      - .env

  redis:
    image: redis:latest

  celery:
    build: .
    command: celery -A credit_system worker --loglevel=info
    depends_on:
      - redis
```
