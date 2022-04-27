FROM python:3.10

ADD . /avro/Message.avsc ./

RUN apt-get update && apt-get install -y \
    librdkafka-dev \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt ./avro/Message.avsc ./

COPY requirements.txt .
RUN pip install -r requirements.txt

#COPY main.py .

COPY avro-consumer.py .

EXPOSE 8080

CMD ["uvicorn", "avro-consumer:app", "--host", "0.0.0.0", "--port", "8080"]

