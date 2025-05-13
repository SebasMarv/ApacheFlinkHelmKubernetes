from pyflink.table.confluent import ConfluentSettings, ConfluentTools
from pyflink.table import (
    EnvironmentSettings,
    StreamTableEnvironment,
    TableDescriptor,
    Schema,
    DataTypes,
)
from pyflink.common import WatermarkStrategy
import json
import logging

env_settings = EnvironmentSettings.in_streaming_mode()
table_env = StreamTableEnvironment.create(environment_settings=env_settings)
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

input_topic = "iot-sensors"
group_id = "flink-postgres-consumer"

confluent_settings = ConfluentSettings.from_file("/opt/flink/usrlib/cloud.properties")

kafka_source_props = ConfluentTools.get_kafka_source_properties(confluent_settings, input_topic, group_id=group_id)

sensor_schema = Schema.new_builder() \
    .column("timestamp", DataTypes.STRING()) \
    .column("sensor_id", DataTypes.STRING()) \
    .column("temperature", DataTypes.FLOAT()) \
    .column("humidity", DataTypes.FLOAT()) \
    .build()

source_table = TableDescriptor.for_connector("kafka") \
    .format("json") \
    .option("topic", input_topic) \
    .options(kafka_source_props) \
    .schema(sensor_schema) \
    .build()

table_env.create_table("raw_iot_data", source_table)

postgres_url = "jdbc:postgresql://host.docker.internal:5435/postgres"
postgres_driver = "org.postgresql.Driver"
postgres_username = "postgres"
postgres_password = "test1234"
postgres_table = "iot_data"

sink_table = TableDescriptor.for_connector("jdbc") \
    .option("url", postgres_url) \
    .option("driver", postgres_driver) \
    .option("username", postgres_username) \
    .option("password", postgres_password) \
    .option("table-name", postgres_table) \
    .schema(sensor_schema).build()

table_env.create_table("postgres_sink", sink_table)

insert_stmt = f"""
INSERT INTO postgres_sink
SELECT
    CAST(TUMBLE_START(TO_TIMESTAMP(timestamp), INTERVAL '1 second') AS TIMESTAMP),
    sensor_id,
    temperature,
    humidity
FROM raw_iot_data
"""

# Ejecutar la consulta de inserción
table_env.execute_sql(insert_stmt).wait()