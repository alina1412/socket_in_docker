FROM python:3.8-slim-buster

RUN mkdir client

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY . ./client

CMD ["python", "-u", "client/app.py"]
