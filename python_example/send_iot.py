from pyflink.table.confluent import ConfluentSettings, ConfluentTools
import json
import random
from datetime import datetime
import time

# Configuración de Confluent Cloud desde el archivo
confluent_settings = ConfluentSettings.from_file("/opt/flink/usrlib/cloud.properties")

# Nombre del topic de entrada
input_topic = "iot-sensors"

if __name__ == '__main__':
    # Configuración del productor de Kafka
    from kafka import KafkaProducer
    producer_props = ConfluentTools.get_kafka_producer_properties(confluent_settings)
    producer = KafkaProducer(
        bootstrap_servers=producer_props['bootstrap.servers'],
        security_protocol=producer_props.get('security.protocol', 'PLAINTEXT'),
        sasl_mechanism=producer_props.get('sasl.mechanism'),
        sasl_plain_username=producer_props.get('sasl.jaas.config', '').split("username='")[1].split("'")[0] if 'username' in producer_props.get('sasl.jaas.config', '') else None,
        sasl_plain_password=producer_props.get('sasl.jaas.config', '').split("password='")[1].split("'")[0] if 'password' in producer_props.get('sasl.jaas.config', '') else None,
        value_serializer=lambda x: json.dumps(x).encode('utf-8')
    )

    try:
        while True:
            timestamp = datetime.utcnow().isoformat() + 'Z'
            sensor_id = f"sensor-{random.randint(1, 10)}"
            temperature = round(random.uniform(20, 90), 2)
            humidity = round(random.uniform(30, 95), 2)
            sensor_data = {
                "timestamp": timestamp,
                "sensor_id": sensor_id,
                "temperature": temperature,
                "humidity": humidity
            }
            producer.send(input_topic, value=sensor_data)
            print(f"Enviando datos ficticios: {sensor_data}")
            time.sleep(1)
    except KeyboardInterrupt:
        print("Deteniendo la generación de datos.")
    finally:
        producer.close()