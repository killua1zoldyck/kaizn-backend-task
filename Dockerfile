# Use an official Python runtime as a parent image
FROM python:3.8

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Install the MySQL client
RUN apt-get update && apt-get install -y default-mysql-client

# Set the working directory
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app/

# Install any needed packages specified in requirements.txt
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

COPY wait-for-db.sh /app/wait-for-db.sh
RUN chmod +x /app/wait-for-db.sh

# Expose port 8000 for Django
EXPOSE 8000

CMD ["./wait-for-db.sh", "db", "python", "kaizn_backend/manage.py", "runserver", "0.0.0.0:8000"]
