FROM python:3.9

ENV PYTHONBUFFERED 1

RUN pip install pipenv==2021.11.15

WORKDIR /code
COPY . /code

RUN pipenv install --system --deploy

EXPOSE 5001

CMD ["python", "-u", "app.py"]