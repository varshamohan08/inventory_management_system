#### inventory_management_system
# Inventory Management System

This repository contains an Inventory Management System built using Django, Django REST Framework, and Redis for caching. It provides user authentication and item management functionalities.

## Table of Contents

- [Installation](#installation)
- [API Endpoints](#api-endpoints)
- [Usage](#usage)

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/varshamohan08/inventory_management_system.git
   cd inventory_management_system
   ```
2. Create a virtual environment and activate it:
   ```
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```
3. Install the required packages:
   ```
    pip install -r requirements.txt
   ```
4. Configure your database settings and Redis settings in settings.py.

   The application connects to Redis using the host and port specified in the Django settings.py file:
   ```
    REDIS_HOST = 'localhost'
    REDIS_PORT = 6379
   ```

6. Run the migrations:
   ```
    python manage.py migrate
   ```
7. Create a superuser to access the Django admin:
   ```
    python manage.py createsuperuser
   ```
8. Start the development server:
   ```
    python manage.py runserver
   ```
9. Start Redis
    ```
    redis-server
    ```

## API Endpoints
api_endpoints.md
### Using Postman Collection
1. Open Postman.
2. Click on the "Import" button in the top left corner.
3. Choose "Raw Text" and paste [postman collection](https://api.postman.com/collections/34745216-bda300d5-43d2-4367-a0f1-0db4366e8f14?access_key=PMAT-01J9Q7JXDH130CMZE16WZQE86E).
4. Click "Continue", then "Import".
## Usage
- **Base URL:** Set the environment variable base_url to the base URL of your API (e.g., http://localhost:8000).
- **Access Token:** After logging in, capture the access_token from the login response and set it as an bearer token in authorization section in Postman for subsequent requests.

