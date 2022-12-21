FROM python:3.8-slim-buster

RUN mkdir receiver


COPY requirements.txt . 
RUN pip install -r requirements.txt

COPY . ./receiver/

CMD ["python", "receiver/receiver.py"]
