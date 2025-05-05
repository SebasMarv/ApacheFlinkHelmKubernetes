# FROM apache/flink:1.13.2
FROM flink:2.0.0

RUN apt-get update -y && \
    apt-get install -y python3 python3-pip python3-dev && \
    pip3 install apache-flink==1.13.2 && \
    # Instalar otras dependencias de tu aplicación
    pip3 install <tus-dependencias>

# Copiar tus scripts de Python
COPY scripts/ /opt/flink/scripts/