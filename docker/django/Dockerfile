FROM python:3.11.9-slim

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONPATH=/app

RUN adduser user \
    && addgroup docker \
    && adduser user docker

COPY requirements.txt /temp/requirements.txt

RUN apt-get update \
    && pip install --upgrade pip \
    && apt-get install -y postgresql \
    && apt-get install -y postgresql-client \
    && apt-get install -y build-essential \
    && apt-get install -y libpq-dev \
    && apt-get install -y gettext \
    && apt-get install -y git \
    && pip install -r /temp/requirements.txt \
    && pip install debugpy -t /tmp \
    && apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false \
    && rm -rf /var/lib/apt/lists/*

COPY ./docker/django/entrypoint /entrypoint
RUN sed -i 's/\r$//g' /entrypoint
RUN chmod +x /entrypoint

COPY ./docker/django/start /start
RUN sed -i 's/\r$//g' /start
RUN chmod +x /start

COPY ./docker/django/celery/worker/start /start-celeryworker
RUN sed -i 's/\r$//g' /start-celeryworker
RUN chmod +x /start-celeryworker

COPY ./docker/django/celery/beat/start /start-celerybeat
RUN sed -i 's/\r$//g' /start-celerybeat
RUN chmod +x /start-celerybeat

RUN mkdir static

WORKDIR /app

RUN chown -R user:user .

USER user

EXPOSE 8000

ENTRYPOINT [ "/entrypoint" ]
