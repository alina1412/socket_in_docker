FROM python:3.8-slim-buster

RUN mkdir sender


COPY requirements.txt . 
RUN pip install -r requirements.txt

COPY . ./sender

CMD ["python", "sender/sender.py"]
