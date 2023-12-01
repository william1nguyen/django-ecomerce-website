FROM python:3.11.2

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

RUN pip install pipenv
COPY Pipfile /app/
COPY Pipfile.lock /app/
RUN pipenv install --system

COPY . /app/
RUN python manage.py collectstatic --noinput

CMD ["python", "manage.py", "runserver", "0.0.0.0:8080"]