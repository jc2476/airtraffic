# Use the official Python image as a parent image
FROM python:3.9

# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install -r requirements.txt

# Expose port 5000 for Gunicorn
EXPOSE 5000

# Run Gunicorn with the provided configuration
CMD ["gunicorn", "--config", "gunicorn_config.py", "app:app"]
