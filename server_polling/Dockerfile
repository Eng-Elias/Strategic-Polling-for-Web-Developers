# Use an official Python runtime as the base image
FROM python:3.11
ENV PYTHONUNBUFFERED=1

# Set the working directory in the container
WORKDIR /usr/src/app

# Copy the requirements file into the container
COPY requirements.txt ./

# Install dependencies
# RUN pip install --no-cache-dir -r requirements.txt
RUN pip install -r requirements.txt

# Expose the port the app runs on
EXPOSE 8000

# Run the command to start the server
# CMD ["gunicorn", "--bind", "0.0.0.0:8000", "server_polling.wsgi:application"]
#ENTRYPOINT ["python", "manage.py"]
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
