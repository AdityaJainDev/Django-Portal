# Use an official Python runtime as a parent image
FROM python:3.8-buster

# Set the working directory to /app
WORKDIR /app

# Packages required to run the app should be built into the image
COPY requirements-frozen.txt /app

#install headless chrome
RUN apt-get update \
    && apt-get install apt-transport-https ca-certificates gettext rsync openssh-client ssh curl -y
# upgrade pip and install any needed packages specified in requirements-frozen.txt
RUN pip install --upgrade pip \
    && pip install --trusted-host pypi.python.org -r requirements-frozen.txt
# Make port 8000 available to the world outside this container
EXPOSE 8000