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
5. Setup database
   
   First, create the PostgreSQL database manually using the command line.

   Open your terminal and access the PostgreSQL prompt
   ```
   sudo -u postgres psql
   ```
   In the PostgreSQL prompt, create the database:
   ```
   CREATE DATABASE inventory_management_system;
   ```
   Create a user and grant them access to the database:
   ```
   CREATE USER your_user_name WITH PASSWORD 'your_password';
   GRANT ALL PRIVILEGES ON DATABASE inventory_management_system TO your_user_name;
   ```
   Exit the PostgreSQL prompt:
   ```
   \q
   ```
   Update [.env](https://github.com/varshamohan08/inventory_management_system/blob/main/.env) file accordingly
7. Run the migrations:
   ```
   python manage.py makemigrations
   python manage.py migrate
   ```
8. Create a superuser to access the Django admin:
   ```
   python manage.py createsuperuser
   ```
9. Start the development server:
   ```
   python manage.py runserver
   ```
10. Start Redis
   ```
   redis-server
   ```

## API Endpoints
api_endpoints.md
### Using Postman Collection
The Postman collection for this project is located in the [inventory_management_system.postman_collection.json](https://github.com/varshamohan08/inventory_management_system/blob/main/inventory_management_system.postman_collection.json) folder.

#### Importing into Postman:
1. Download the [inventory_management_system.postman_collection.json](https://github.com/varshamohan08/inventory_management_system/blob/main/inventory_management_system.postman_collection.json) file from this repository.
2. Open Postman, click **Import**, and choose the downloaded file.
3. The collection will appear in your Postman workspace.

## Usage
- **Base URL:** Set the environment variable base_url to the base URL of your API (e.g., http://localhost:8000).
- **Access Token:** After logging in, capture the access_token from the login response and set it as an bearer token in authorization section in Postman for subsequent requests.

