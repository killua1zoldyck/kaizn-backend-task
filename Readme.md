# Project Name

Take home task for Kaizntree

## Prerequisites

Before you begin, ensure you have met the following requirements:

- Docker Compose

## Getting Started

To get the project up and running, follow these steps:

1. **Clone the repository:**
    ```bash
    git clone git@github.com:killua1zoldyck/kaizn-backend-task.git
    ```

2. **Navigate to the project directory:**
    ```bash
    cd backend
    ```

3. **Run Docker Compose to build and start the application:**
    ```bash
    docker-compose up --build
    ```

4. **Access the application at [http://localhost:8000](http://localhost:8000)**



## Running Tests

To run tests, use the following command:

```bash
docker-compose exec web python kaizn_backend/manage.py test kaizn_app
```
