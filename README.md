# FastAPI User & Transaction Management API

This project provides a user and transaction management system built with FastAPI and SQLAlchemy, utilizing asynchronous database operations. It allows for efficient creation, retrieval, and management of users and their transactions, designed with performance and scalability in mind.

## Features

- User Management: Create and retrieve user information with unique usernames.
- Transaction Management: Add and fetch transactions linked to users.
- Asynchronous Database Operations: Powered by SQLAlchemy's async capabilities for non-blocking I/O.
- Pydantic Validation: Data validation and serialization with Pydantic.
- Logging: Detailed logging for debugging and tracking operations.
- Static Files Handling: Serve static files such as images or documents.

## Technology Stack

- Backend Framework: FastAPI
- Database ORM: SQLAlchemy (Async Support)
- PostgreSQL: Database management system
- Pydantic: Data validation and parsing
- Logging: Integrated for tracking app events

## Installation & Setup

### Prerequisites

- Python 3.8+
- Docker and Docker Compose

## Step 1: Clone the Repository

    ```bash
    git clone git@github.com:igor20192/TransactiTrack.git
    ```
    ```bash
    cd TransactiTrack
    ```

## Step 2: Set Up PostgreSQL with Docker
  
Ensure Docker is running, then start PostgreSQL using Docker Compose:

1. Create a docker-compose.yml file in the project root with the following content:

```yaml
services:
  db:
    image: postgres:17rc1-alpine
    volumes:
      - postgres_data:/var/lib/postgresql/data/
    env_file:
      - .env.db
    ports:
      - 5432:5432


volumes:
  postgres_data:
  ```

2. Start the PostgreSQL container:

   ```bash
   docker-compose up -d
   ```

## Step 3: Create and Activate Virtual Environment

Create a virtual environment and activate it:

    ```bash 
    python -m venv venv
    source venv/bin/activate  # On Windows use: venv\Scripts\activate
    ```

## Step 4: Install Dependencies

    ```bash
    pip install -r requirements.txt
    ```

## Step 5: Configure Environment Variables

Create a .env file in the project root with the following content:

    ```plaintext
    DATABASE_USERNAME=your_postgres_username
    DATABASE_PASSWORD=your_postgres_password
    DATABASE_NAME=your_database_name
    ```

## Step 6: Apply Database Migrations

Ensure your PostgreSQL database is running and then apply migrations:

    ```bash
    alembic upgrade head
    ```

## Step 7: Run the Application

Start the FastAPI server:

    ```bash
    uvicorn app.main:app --reload
    ```

The API will be available at http://127.0.0.1:8000.

## API Endpoints

### User Endpoints

1. Create User

    - POST /users/
    - Request Body:
        ```json
        {
            "username": "newuser"
        }
        ```
    - Response:
        ```json
        {
           "id": 1
        }
        ```

2. Get User by ID

    - GET /users/{user_id}
    - Response:
    ```json
       {
        "id": 1,
        "username": "newuser",
        "transactions": []
       }
       ```

3. Get All Users
 
    - GET /users/
    - Response:

    ```json
       [
       {
        "id": 1,
        "username": "newuser",
        "transactions": []
       }
       ]
       ```

## Transaction Endpoints

1. Add Transaction

    - POST /transactions/
    - Request Body:
    ```json
       {
        "user_id": 1,
        "type": "credit",
        "amount": 100.0
        }
    ```

    - Response:
    ```json
    {
        "id": 1,
        "user_id": 1,
        "type": "credit",
        "amount": 100.0,
        "timestamp": "2023-10-10T10:00:00"
    }
    ```

2. Get Transactions for User

    - GET /users/{user_id}
    - Response:

    ```json
    [
       {
            "id": 1,
            "type": "credit",
            "amount": 100.0,
            "timestamp": "2023-10-10T10:00:00"
       }
    ]
    ```

## Project Structure

```bash
.
├── app/
│   ├── __init__.py
│   ├── main.py               # FastAPI app initialization and routing
│   ├── crud.py               # Database operations (Create, Read, Update, Delete)
│   ├── models.py             # SQLAlchemy models (User, Transaction)
│   ├── schemas.py            # Pydantic models for request and response validation
│   ├── database.py           # Database connection setup and session management
│   ├── admin.py              # Admin routes (optional)
├── static/                   # Static files served by the app
├── alembic/                  # Database migration files
├── docker-compose.yml        # Docker Compose configuration for PostgreSQL
├── .env                      # Environment variables for database credentials
├── README.md
└── requirements.txt
```

## Pydantic Schemas

- ### User:
    - id (int): User's unique identifier.
    - username (str): User's username.
    - transactions (List[Transaction]): List of user's transactions.
- ### Transaction:
    - id (int): Transaction's unique identifier.
    - type (str): Transaction type (e.g., "credit", "debit").
    - amount (float): Transaction amount.
    - timestamp (datetime): Transaction timestamp.


## Logging

Logging is set up at the DEBUG level to track application flow and errors. Logs include information on:

- User creation and retrieval
- Transaction addition and retrieval
- Errors during database operations

## Contributing

- Fork the repository.
- Create a new branch (git checkout -b feature-branch).
- Make your changes.
- Commit your changes (git commit -m 'Add feature').
- Push to the branch (git push origin feature-branch).
- Create a pull request.

## License

This project is licensed under the MIT License.

















