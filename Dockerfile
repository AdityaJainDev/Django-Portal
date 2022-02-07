# Use an official Python runtime as a parent image
FROM python:3.7-buster

# Set the working directory to /app
WORKDIR /app

# Packages required to run the app should be built into the image
COPY requirements-frozen.txt /app

#install headless chrome
RUN apt-get update \
    && apt-get install apt-transport-https ca-certificates gettext -y \
    && wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add - \
    && sh -c 'echo "deb https://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google.list' \
    && apt-get update \
    && apt-get install google-chrome-stable -y \
    && wget https://chromedriver.storage.googleapis.com/2.41/chromedriver_linux64.zip \
    && unzip chromedriver_linux64.zip \
    && mv chromedriver /usr/local/bin

# upgrade pip and install any needed packages specified in requirements-frozen.txt
RUN pip install --upgrade pip \
    && pip install --trusted-host pypi.python.org -r requirements-frozen.txt

# Make port 8000 available to the world outside this container
EXPOSE 8000