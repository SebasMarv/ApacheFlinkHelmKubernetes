from kafka import KafkaProducer
import json
import time

# Configuración de Kafka (Confluent)
KAFKA_BROKER = 'pkc-619z3.us-east1.gcp.confluent.cloud:9092'  # Dirección del broker
TOPIC = 'test-topic'  # Nombre del tópico
SASL_USERNAME = '4INZQR6SVQ42QHQM'  # Tu API Key
SASL_PASSWORD = 'mUhX+eIzA9JgIuUp1RepDjzDpFoP+6pfOpTqrGg2AJV6Dt4hqghjFFKMTBSDXzZi'  # Tu API Secret

# Crear un productor de Kafka
producer = KafkaProducer(
    bootstrap_servers=KAFKA_BROKER,
    security_protocol="SASL_SSL",
    sasl_mechanism="PLAIN",
    sasl_plain_username=SASL_USERNAME,
    sasl_plain_password=SASL_PASSWORD,
    value_serializer=lambda v: json.dumps(v).encode('utf-8'),
    request_timeout_ms=20000,  # Tiempo de espera de 20 segundos
    retries=5  # Reintentar 5 veces en caso de error
)

# Generar y enviar mensajes
try:
    for i in range(10):  # Envía 10 mensajes como ejemplo
        message = {'id': i, 'message': f'Mensaje {i}'}
        producer.send(TOPIC, value=message)
        print(f'Mensaje enviado: {message}')
        time.sleep(1)  # Espera 1 segundo entre mensajes
finally:
    producer.close()