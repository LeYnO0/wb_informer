FROM python:3.10-slim

RUN mkdir project

WORKDIR wb_informer

ADD . /wb_informer/
ADD .env /wb_informer/.env

RUN pip install -r requirements.txt
EXPOSE 5432

CMD ["python", "main.py"]