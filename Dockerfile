FROM python:3.6

WORKDIR /app
ADD . .
RUN pip install -r requirements/production.txt

ENTRYPOINT celery worker -A opulence.collectors.app --queues=collectors --loglevel=info --hostname=collector_1@%h
