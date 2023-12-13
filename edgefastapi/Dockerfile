ARG EDGEFASTAPI_PORT
FROM python:3.9

WORKDIR /app


RUN apt-get update
RUN apt-get install -y python3-distutils ffmpeg



COPY ./requirements.txt /app/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt

EXPOSE ${EDGEFASTAPI_PORT}
