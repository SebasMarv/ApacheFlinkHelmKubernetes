# from pyflink.datastream import StreamExecutionEnvironment
# from pyflink.datastream.connectors import FlinkKafkaProducer
# from pyflink.common.serialization import SimpleStringSchema
# import json
# import random
# from datetime import datetime

# # Configuración del tópico y broker Kafka
# KAFKA_BROKER = 'pkc-619z3.us-east1.gcp.confluent.cloud:9092'
# TOPIC = 'iot-sensors'

# # Configuración de autenticación para Confluent Kafka
# KAFKA_PRODUCER_CONFIG = {
#     'bootstrap.servers': KAFKA_BROKER,
#     'security.protocol': 'SASL_SSL',
#     'sasl.mechanism': 'PLAIN',
#     'sasl.username': '4INZQR6SV42QHQM',
#     'sasl.password': 'mUhX+eIzA9JgIuUp1RepDjzDpFoP+6pfOpTqrGg2AJV6Dt4hqghjFFKMTBSDXzZi'
# }

# def generate_sensor_data():
#     """Genera datos ficticios de sensores."""
#     timestamp = datetime.utcnow().isoformat() + 'Z'
#     sensor_id = f"sensor-{random.randint(1, 10)}"
#     temperature = round(random.uniform(20, 90), 2)
#     humidity = round(random.uniform(30, 95), 2)
#     return json.dumps({
#         "timestamp": timestamp,
#         "sensor_id": sensor_id,
#         "temperature": temperature,
#         "humidity": humidity
#     })

# def main():
#     env = StreamExecutionEnvironment.get_execution_environment()

#     # Crear un productor de Kafka con un esquema de serialización válido
#     kafka_producer = FlinkKafkaProducer(
#         topic=TOPIC,
#         serialization_schema=SimpleStringSchema(),  # Usar un esquema de serialización válido
#         producer_config=KAFKA_PRODUCER_CONFIG
#     )

#     # Generar datos ficticios y enviarlos a Kafka
#     data_stream = env.from_collection([generate_sensor_data() for _ in range(10)])
#     data_stream.add_sink(kafka_producer)

#     env.execute("Send IoT Data to Kafka")

# if __name__ == "__main__":
#     main()

# ---------------------------------------------------

# from pyflink.common import Configuration
# from pyflink.datastream import StreamExecutionEnvironment
# from pyflink.datastream.connectors import FlinkKafkaProducer
# from pyflink.common.serialization import SimpleStringSchema

# KAFKA_BROKER = 'pkc-619z3.us-east1.gcp.confluent.cloud:9092'
# TOPIC = 'iot-sensors'

# KAFKA_PRODUCER_CONFIG = {
#     'bootstrap.servers': KAFKA_BROKER,
#     'security.protocol': 'SASL_SSL',
#     'sasl.mechanism': 'PLAIN',
#     'sasl.username': '4INZQR6SVQHQM',
#     'sasl.password': 'mUhX+eIzA9JgIuUp1RepDjzDpFoP+6pfOpTqrGg2AJV6Dt4hqghjFFKMTBSDXzZi'
# }

# def main():
#     config = Configuration()
#     # config.set_string("pipeline.jars", "file:///opt/flink/lib/flink-connector-kafka.jar")
#     config.set_string("pipeline.jars", "opt/flink/lib/flink-connector-kafka.jar")
#     env = StreamExecutionEnvironment.get_execution_environment(configuration=config)

#     kafka_producer = FlinkKafkaProducer(
#         topic=TOPIC,
#         serialization_schema=SimpleStringSchema(),  # Serialización simple
#         producer_config=KAFKA_PRODUCER_CONFIG
#     )

#     data_stream = env.from_collection(["mensaje_minimo"])

#     data_stream.add_sink(kafka_producer)

#     env.execute("Enviar mensaje mínimo a Kafka")

# if __name__ == "__main__":
#     main()


# ---------------------------------------------------

from pyflink.table import EnvironmentSettings, TableEnvironment, DataTypes
from pyflink.table.descriptors import Kafka, Schema
from pyflink.table import StreamTableEnvironment
from pyflink.datastream import StreamExecutionEnvironment

# Configuración del broker Kafka y tópico
KAFKA_BROKER = 'pkc-619z3.us-east1.gcp.confluent.cloud:9092'
TOPIC = 'iot-sensors'

# Configuración de autenticación para Confluent Kafka
KAFKA_PRODUCER_CONFIG = {
    'bootstrap.servers': KAFKA_BROKER,
    'security.protocol': 'SASL_SSL',
    'sasl.mechanism': 'PLAIN',
    'sasl.username': '4INZQR6SVQHQM',
    'sasl.password': 'mUhX+eIzA9JgIuUp1RepDjzDpFoP+6pfOpTqrGg2AJV6Dt4hqghjFFKMTBSDXzZi'
}

def main():
    # Crear el entorno de ejecución de la Table API
    env = StreamExecutionEnvironment.get_execution_environment()
    env.set_parallelism(1)
    table_env = StreamTableEnvironment.create(stream_execution_environment=env)

    # Configurar el conector de Kafka como un sink
    table_env.connect(
        Kafka()
        .version("universal")
        .topic(TOPIC)
        .property("bootstrap.servers", KAFKA_BROKER)
        .property("security.protocol", "SASL_SSL")
        .property("sasl.mechanism", "PLAIN")
        .property("sasl.username", "4INZQR6SVQHQM")
        .property("sasl.password", "mUhX+eIzA9JgIuUp1RepDjzDpFoP+6pfOpTqrGg2AJV6Dt4hqghjFFKMTBSDXzZi")
    ).with_format(
        Schema()
        .field("message", DataTypes.STRING())
    ).with_schema(
        Schema()
        .field("message", DataTypes.STRING())
    ).create_temporary_table("kafka_sink")

    # Crear una tabla de ejemplo con datos
    table_env.execute_sql("""
        INSERT INTO kafka_sink
        SELECT 'Mensaje de prueba desde Flink'
    """)

if __name__ == "__main__":
    main()