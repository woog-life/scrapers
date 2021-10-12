FROM python:3.10-slim

WORKDIR /usr/src/app

ENV TZ=Europe/Berlin

RUN apt update && apt install -y gcc libffi-dev && rm -rf /var/lib/apt/lists/*

ADD . .
ADD requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

RUN sed -i -e "s/'utf-8'/'ISO-8859-1'/g" /usr/local/lib/python3.10/site-packages/scrapy/robotstxt.py

CMD python -B -O main.py
