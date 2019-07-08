FROM python:3
ENV PYTHONUNBUFFERED 1
RUN mkdir /code
WORKDIR /code
RUN apt-get update && apt-get install -y git
RUN git clone https://github.com/otterlogic/mock-weather-api .
RUN pip install -r requirements.txt
