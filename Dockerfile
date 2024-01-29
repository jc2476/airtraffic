# Use an official Python runtime as the base image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /usr/src/app

# Copy the current directory contents into the container
COPY . .

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Make Gunicorn bind to 0.0.0.0:5000 and start 3 worker processes
CMD ["gunicorn", "-b", "0.0.0.0:5000", "-w", "3", "app:app"]
# 'app:app' refers to `<module_name>:<Flask_app_object>`. Ensure this matches your Flask app's structure.