FROM python:3.6

WORKDIR /usr/src/app

COPY requirements.txt ./
COPY getInformation.py /usr/src/app
COPY server.py /usr/src/app
ENV FLASK_APP server.py
RUN pip install --no-cache-dir -r requirements.txt
COPY . /usr/src/app
