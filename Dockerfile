FROM python:3.8-slim-buster

WORKDIR /
ENV TOKEN=YOUR_TOKEN
#Insert IP for external MySQL Server
ENV DB.HOST=localhost
ENV DB.PW='YOUR_DB_PASSWORD'
ENV DB='YOUR_DATABASE'
#ENV DB.PORT='YOUR_PORT'

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . .

RUN mkdir downloads
RUN apt-get update && apt-get install -y ffmpeg

CMD ["python3", "main.py"]
