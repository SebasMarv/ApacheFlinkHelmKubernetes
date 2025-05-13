from pyflink.table import EnvironmentSettings, TableEnvironment
from pyflink.table.descriptors import Kafka, Json, Schema
from pyflink.table.descriptors import Jdbc
from pyflink.table import DataTypes

# Configuración del tópico y broker de Kafka
KAFKA_BROKER = 'pkc-619z3.us-east1.gcp.confluent.cloud:9092'
TOPIC = 'iot-sensors'

# Configuración de PostgreSQL
POSTGRES_URL = "jdbc:postgresql://host.docker.internal:5435/postgres"
POSTGRES_DRIVER = "org.postgresql.Driver"
POSTGRES_USERNAME = "postgres"
POSTGRES_PASSWORD = "test1234"
POSTGRES_TABLE = "iot_data"

def main():
    # Crear el entorno de Flink
    env_settings = EnvironmentSettings.in_streaming_mode()
    table_env = TableEnvironment.create(environment_settings=env_settings)

    # Configurar el conector de Kafka
    table_env.connect(
        Kafka()
        .version("universal")
        .topic(TOPIC)
        .property("bootstrap.servers", KAFKA_BROKER)
        .property("security.protocol", "SASL_SSL")
        .property("sasl.mechanism", "PLAIN")
        .property("sasl.username", "4INZQR6SVQ42QHQM")
        .property("sasl.password", "mUhX+eIzA9JgIuUp1RepDjzDpFoP+6pfOpTqrGg2AJV6Dt4hqghjFFKMTBSDXzZi")
    ).with_format(
        Json()
        .fail_on_missing_field(False)
        .derive_schema()
    ).with_schema(
        Schema()
        .field("timestamp", DataTypes.STRING())
        .field("sensor_id", DataTypes.STRING())
        .field("temperature", DataTypes.FLOAT())
        .field("humidity", DataTypes.FLOAT())
    ).create_temporary_table("kafka_source")

    # Configurar el conector de PostgreSQL
    table_env.connect(
        Jdbc()
        .url(POSTGRES_URL)
        .table(POSTGRES_TABLE)
        .driver(POSTGRES_DRIVER)
        .username(POSTGRES_USERNAME)
        .password(POSTGRES_PASSWORD)
    ).with_schema(
        Schema()
        .field("timestamp", DataTypes.STRING())
        .field("sensor_id", DataTypes.STRING())
        .field("temperature", DataTypes.FLOAT())
        .field("humidity", DataTypes.FLOAT())
    ).create_temporary_table("postgres_sink")

    # Leer datos de Kafka y escribirlos en PostgreSQL
    table_env.from_path("kafka_source").insert_into("postgres_sink")
    table_env.execute("Consume IoT Data from Kafka and Store in PostgreSQL")

if __name__ == "__main__":
    main()