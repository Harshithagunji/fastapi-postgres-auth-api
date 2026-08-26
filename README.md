
# FastAPI Bookstore API

A production-ready RESTful Bookstore API built with FastAPI, PostgreSQL, SQLAlchemy 2.0, Alembic, and Docker.

## Tech Stack
- **Framework:**FastAPI
- **Database:**PostgreSQL with SQLAlchemy 2.0 ORM
- **Migrations:**Alembic
- **containerization:**Docker& Docker Compose
- **Testing:**pytest

## Getting Started

## Prerequisites
-Docker Desktop installed and running.

### Installation & Running with Docker
1. Clone the repository and navigate into project directory.
2. Create a `.env` file in the root directory with your configuration:
    ```env
   
   SQLALCHEMY_DATABASE_URL='postgresql://postgres:123456@db:5432/bookstore'
   SECRET_KEY= 'super_secret_key_change_in_production'
   ALGORITHM=HS256
   ACCESS_TOKEN_EXPIRE_MINUTES=30