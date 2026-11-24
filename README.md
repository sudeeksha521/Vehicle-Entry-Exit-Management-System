# Vehicle Entry & Exit Management System

## Project Overview
The Vehicle Entry & Exit Management System is a Django-based backend application designed for construction companies to manage vehicle movements at their construction sites.

It digitizes the manual vehicle entry and exit process and maintains vehicle movement records in a PostgreSQL database.

## Technologies Used
- Python
- Django
- Django REST Framework
- PostgreSQL
- Postman
- VS Code

## Main Features
- Vehicle registration and management
- Vehicle entry recording
- Vehicle exit recording
- Prevention of duplicate active entries
- Vehicle re-entry after exit
- Vehicle movement history
- Currently inside vehicle list
- Daily vehicle reports
- User authentication
- Automated API testing

## Project Structure

```text
VehicleEntryExitProject/
│
├── config/
├── vehicles/
│   ├── migrations/
│   ├── models.py
│   ├── serializers.py
│   ├── views.py
│   ├── urls.py
│   └── tests.py
│
├── manage.py
├── requirements.txt
├── .env.example
├── .gitignore
└── README.md
```

## Installation and Setup

1. Clone the repository.
2. Create and activate a virtual environment.
3. Install the required packages:

```bash
pip install -r requirements.txt
```

4. Create a `.env` file using `.env.example` and configure your PostgreSQL database credentials.

5. Run database migrations:

```bash
python manage.py migrate
```

6. Create an administrator account:

```bash
python manage.py createsuperuser
```

7. Start the development server:

```bash
python manage.py runserver
```

8. Open `http://127.0.0.1:8000/` in your browser.

## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/api/vehicles/` | List vehicles |
| POST | `/api/vehicles/` | Register vehicle |
| GET | `/api/vehicles/{id}/` | View vehicle details |
| PUT/PATCH | `/api/vehicles/{id}/` | Update vehicle |
| POST | `/api/entries/` | Record vehicle entry |
| GET | `/api/entries/` | View vehicle history |
| POST | `/api/entries/{id}/exit/` | Record vehicle exit |
| GET | `/api/entries/inside/` | View vehicles currently inside |
| GET | `/api/reports/daily/?date=YYYY-MM-DD` | Generate daily report |

## Authentication

The APIs require authentication. Basic Authentication and Session Authentication are configured using Django REST Framework.

## Automated Testing

Run the automated tests using:

```bash
python manage.py test vehicles
```

The project includes 10 automated API tests covering vehicle registration, duplicate prevention, entry, exit, re-entry, currently inside vehicles, and daily reports.

## Database

PostgreSQL is used to store vehicle information and vehicle movement records.

## Future Enhancements
- Frontend dashboard
- Export daily reports
- Search and advanced filtering
- User role management

## Author
Project developed as a Django and PostgreSQL backend application.