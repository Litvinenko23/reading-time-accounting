# Reading Time Tracking System

## Description

This system is designed to track the time users spend reading books. Users have the ability to start a reading session, end it, and the system keeps track of the duration of each session and the total reading time for each book.

## Features

### 1. API for Reading Time Tracking

Using Django REST Framework (DRF), the system provides an API that allows:

- Retrieving a list of books with information (title, author, publication year, short description).
- Getting book details (title, author, publication year, short description, full description, date of the last reading).
- Starting and ending a reading session by specifying the book ID. Each user has their own session. A user cannot start more than one session with the same book; if the user starts a session with a different book, the session with the previous book should end automatically.
- Retrieving total reading time for each book and overall user statistics.

### 2. Asynchronous Task Using Celery

A task is created to collect statistics of the total reading time for a user over the last 7 and 30 days, and stores it in the user's profile.

### 3. Testing

Using Pytest, tests are written to verify some aspects of the API.

### 4. Additional features

- User authentication and authorization to the API.
- Swagger documentation
- Dockerization for the application.


## How to run

To run the project, follow these steps:

1. Clone the repository to your computer.

2. Download and install Docker and Docker Compose if they are not already installed.

3. Copy .env.sample -> .env and populate with all required data

4. In the project's root directory, run the following command to start the Docker containers:
```
docker-compose up --build
```

