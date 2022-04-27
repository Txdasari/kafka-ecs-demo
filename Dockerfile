FROM python:3.10

ADD avro-consumer.py .

ADD . /avro/Message.avsc ./

RUN apt-get update && apt-get install -y \
    librdkafka-dev \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt ./avro/Message.avsc ./

RUN pip3 install --no-cache-dir -r requirements.txt

CMD [ "python","./avro-consumer.py" ]

