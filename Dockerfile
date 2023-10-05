FROM python:3.10.12-alpine
WORKDIR /jobspeedyup
COPY . /jobspeedyup
RUN pip install -r requirements.txt
EXPOSE 8000
CMD python manage.py runserver  