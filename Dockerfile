FROM python:3.11-slim

WORKDIR /usr/src/app

ENV TZ=Europe/Berlin

RUN apt update && apt install -y gcc libffi-dev && rm -rf /var/lib/apt/lists/*

ADD . .
ADD requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

CMD python -B -O main.py
