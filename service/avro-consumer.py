from confluent_kafka.schema_registry import SchemaRegistryClient
from configparser import ConfigParser
from confluent_kafka import DeserializingConsumer,SerializingProducer
from confluent_kafka.schema_registry.avro import AvroDeserializer
from email.message import Message


key_schema = """ 
    {"type": "string"}
    """
with open('avro/Message.avsc') as f:
  value_schema = f.read()


topic = 'avro_consumer_test'
schemaurl = "https://psrc-o2wjx.us-east-2.aws.confluent.cloud"
schema_key = "EDKNVGDYYFEEKUOR"
schema_secret = "eoDP7BoVlKCxLye+c5Ip5FuXXjLtUe3Rt57nfPBeYUKWdI73v2VYwPHlvscYfi/j"
group_id= "test_group"

registry = SchemaRegistryClient({
  "url": schemaurl,
  "basic.auth.user.info": f'{schema_key}:{schema_secret}'
})

key_deserializer = AvroDeserializer(registry, key_schema)
value_deserializer = AvroDeserializer(registry, value_schema, from_dict = lambda obj, _:Message(obj))
# Parse the configuration.
# See https://github.com/edenhill/librdkafka/blob/master/CONFIGURATION.md
config_parser = ConfigParser()
with open('client.ini') as f:
  config_parser.read_file(f)
  config = dict(config_parser['default'])


config['key.deserializer'] = key_deserializer 
config['value.deserializer'] = value_deserializer
config['group.id'] = group_id

consumer = DeserializingConsumer(config)
consumer.subscribe([topic])

for i in range(10):
  value = {'my_field1': i, 'my_field2': f'{i}'}
  try:
    msg = consumer.poll(1.0)
  except Exception as e:
    print(f"Exception while consuming record value - {value} topic - {topic}: {e}")
  else:
      print(f"Received message - {value}")

consumer.close()
