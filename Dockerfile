FROM python:3.10-slim-buster

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . .



RUN python3 manage.py makemigrations
RUN python3 manage.py migrate
RUN python3 manage.py seed
RUN echo "yes" | python3 manage.py collectstatic

CMD ["uvicorn", "app.delivery.web.asgi:application", "--host", "0.0.0.0", "--port", "8000"]

