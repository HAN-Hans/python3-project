# Use an official Python runtime as a parent image
FROM python:2.7-slim

# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
ADD . /app

# Install any needed packages specified in requirements.txt
<<<<<<< HEAD
<<<<<<< HEAD
RUN pip install -i https://pypi.douban.com/simple -r requirements.txt
=======
RUN pip install --trusted-host pypi.python.org -r requirements.txt
>>>>>>> celery
=======
RUN pip install --trusted-host pypi.python.org -r requirements.txt
=======
RUN pip install -i https://pypi.douban.com/simple -r requirements.txt
>>>>>>> 0816511addce92eb8bc140ce93ef180061bab02e
>>>>>>> celery

# Make port 80 available to the world outside this container
EXPOSE 80

# Define environment variable
ENV NAME World

# Run app.py when the container launches
<<<<<<< HEAD
CMD ["python", "app.py"]
=======
CMD ["python", "app.py"]
<<<<<<< HEAD
>>>>>>> celery
=======
>>>>>>> 0816511addce92eb8bc140ce93ef180061bab02e
>>>>>>> celery
