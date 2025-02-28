# Task Management API

A simple RESTful API for managing tasks (ToDo List) built using **FastAPI**, **SQLAlchemy** and **SQLite** as the database.

## Features

- **CRUD** operations for tasks (Create, Read, Update, Delete).
- **Authentication** (Basic Auth).
- **Test Coverage** using **Pytest**.
- **Docker** support for easy deployment.
- **Swagger UI** auto-generated documentation.

## Technologies Used

- **FastAPI**: Modern, fast web framework for building APIs with Python 3.11+ based on standard Python type hints.
- **SQLAlchemy**: ORM for interacting with databases.
- **SQLite**: Lightweight, file-based relational database used for development.
- **Pytest**: Framework for testing the application.
- **Docker**: Containerization of the application

## Prerequisites

Before starting the project, ensure you have the following installed:

- Python 3.11
- **Docker** 
- **Git** (for version control)

## Setup and Installation

### 1. Clone the repository
```bash
git clone https://github.com/AnaK57/TodoRestApi.git
cd TodoRestApi
```
### 2. create and activate virtual environmnent
```bash
python3 -m venv venv
venv\Scripts\activate  # On Linux/macOS: source venv/bin/activate
```
### 3. install dependencies
```bash
pip install -r requirements.txt
```
### To run the application locally, use the following command:
```bash
uvicorn app.main:app --reload
```
The API will be available at http://127.0.0.1:8000.

### If you prefer using Docker, you can run the following command to start the app in a Docker container:
```bash
docker-compose up --build
```
The API will be available at http://127.0.0.1:8000.

## API Endpoints
- GET /tasks: Get a list of all tasks.
- GET /tasks/{task_id}: Get a specific task by ID. 
- POST /tasks: Create a new task.
- PUT /tasks/{task_id}: Update an existing task by ID.
- DELETE /tasks/{task_id}: Delete a task by ID.

## Swagger UI
Once the application is running, you can access the Swagger UI documentation at:
http://127.0.0.1:8000/docs