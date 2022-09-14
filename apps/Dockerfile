# FROM python:3.9

# COPY . .

# # set environment variables
# ENV PYTHONDONTWRITEBYTECODE 1
# ENV PYTHONUNBUFFERED 1

# # dependencias sistema operativo
# #RUN apt-get update && apt-get install -y apt-utils gcc build-essential musl-dev python3-dev vim nano

# # install python dependencies
# RUN pip install --upgrade pip
# RUN pip install --upgrade setuptools
# RUN pip install -r requirements.txt
# #RUN pip install --no-cache-dir -r requirements.txt

# #COPY . .

# # running migrations
# RUN python manage.py migrate

# # gunicorn
# CMD ["gunicorn", "--config", "gunicorn-cfg.py", "core.wsgi"]

# Imagen oficial Docker Hub python3.8

FROM python:3.9

# directorio de trabajo
WORKDIR /usr/src/apps

# variables de entorno
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# dependencias sistema operativo
RUN apt-get update && apt-get install -y apt-utils gcc build-essential musl-dev python3-dev vim nano ffmpeg libglib2.0-0 libsm6 libxext6 libfontconfig1 libxrender1 libgl1-mesa-glx
RUN pip install opencv-python

# dependencias App
RUN pip install --upgrade pip
RUN pip install --upgrade setuptools


COPY ./requirements.txt .
RUN pip install -r requirements.txt

# copiar proyecto a contenedor
COPY . .

# # running migrations
RUN python manage.py makemigrations
RUN python manage.py migrate