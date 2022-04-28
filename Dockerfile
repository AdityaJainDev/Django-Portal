# Use an official Python runtime as a parent image
FROM python:3.8-alpine

# Set the working directory to /app
WORKDIR /app

# Packages required to run the app should be built into the image
COPY requirements-frozen.txt /app

ENV MUSL_LOCPATH="/usr/share/i18n/locales/musl"

#install headless chrome
RUN set -ex \
    && apk add --no-cache --virtual .build-deps gcc build-base musl-dev mariadb-connector-c-dev libffi-dev \
    && apk add gettext-dev \
    musl-locales \
    musl-locales-lang \
    && python -m venv /env \
    && /env/bin/pip install --upgrade pip \
    && /env/bin/pip install --no-cache-dir -r /app/requirements-frozen.txt \
    && runDeps="$(scanelf --needed --nobanner --recursive /env \
        | awk '{ gsub(/,/, "\nso:", $2); print "so:" $2 }' \
        | sort -u \
        | xargs -r apk info --installed \
        | sort -u)" \
    && apk add --virtual rundeps $runDeps \
    && apk del .build-deps

ENV VIRTUAL_ENV=/env PATH=/env/bin:$PATH

#Copy project to App
COPY . /app

# Make port 8000 available to the world outside this container
EXPOSE 8000

RUN python manage.py collectstatic --noinput && django-admin compilemessages

CMD ["gunicorn", "-c", "gunicorn.py"]
