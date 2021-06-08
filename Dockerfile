FROM python:3.9

WORKDIR /app

COPY ./requirements.txt ./

RUN apt-get update

RUN apt-get install -y python3-pip

RUN pip3 install -r requirements.txt

COPY ./ ./

CMD uvicorn app:app --workers 4 --host 0.0.0.0 --port 3000