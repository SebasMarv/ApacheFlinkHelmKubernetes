FROM flink:1.16
#FROM apache/flink:2.0.0
# install python3: it has updated Python to 3.9 in Debian 11 and so install Python 3.7 from source, \
# it currently only supports Python 3.6, 3.7 and 3.8 in PyFlink officially.

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libssl-dev \
    zlib1g-dev \
    libbz2-dev \
    libffi-dev \
    liblzma-dev \
    wget \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

RUN apt-get update -y && \
apt-get install -y build-essential libssl-dev zlib1g-dev libbz2-dev libffi-dev && \
wget https://www.python.org/ftp/python/3.7.9/Python-3.7.9.tgz && \
tar -xvf Python-3.7.9.tgz && \
cd Python-3.7.9 && \
./configure --without-tests --enable-shared && \
make -j6 && \
make install && \
ldconfig /usr/local/lib && \
cd .. && rm -f Python-3.7.9.tgz && rm -rf Python-3.7.9 && \
ln -s /usr/local/bin/python3 /usr/local/bin/python && \
apt-get clean && \
rm -rf /var/lib/apt/lists/*

# install PyFlink
# RUN pip3 install "apache-flink>=1.16.0,<1.17.1"

RUN pip3 install "apache-flink==1.16.3"
RUN pip3 install kafka-python

# # Agregar el repositorio oficial de Confluent y su clave GPG
# RUN apt-get update && apt-get install -y --no-install-recommends \
#     wget \
#     software-properties-common && \
#     wget -qO - https://packages.confluent.io/deb/7.3/archive.key | apt-key add - && \
#     add-apt-repository "deb [arch=amd64] https://packages.confluent.io/deb/7.3 stable main" && \
#     apt-get update && apt-get install -y --no-install-recommends \
#     librdkafka-dev \
#     gcc \
#     g++ \
#     && apt-get clean && rm -rf /var/lib/apt/lists/*

# Instalar confluent-kafka compatible con Python 3.7
RUN pip3 install "confluent-kafka==1.9.2"

#RUN pip3 install "apache-flink==2.0.0"
# download flink connectors
# flink-connector-kafka, flink-connector-jdbc and postgresql driver
RUN mkdir -p /opt/flink/lib
RUN curl -o /opt/flink/lib/flink-connector-kafka.jar https://repo1.maven.org/maven2/org/apache/flink/flink-connector-kafka/2.0.0/flink-connector-kafka-2.0.0.jar && \
    curl -o /opt/flink/lib/flink-connector-jdbc.jar https://repo1.maven.org/maven2/org/apache/flink/flink-connector-jdbc/2.0.0/flink-connector-jdbc-2.0.0.jar && \
    curl -o /opt/flink/lib/postgresql-driver.jar https://repo1.maven.org/maven2/org/postgresql/postgresql/42.5.0/postgresql-42.5.0.jar
# add python script
USER flink
RUN mkdir /opt/flink/usrlib
# Pipelines de IOT
ADD python_example/receptor_iot.py /opt/flink/usrlib/receptor_iot.py
ADD python_example/send_iot.py /opt/flink/usrlib/send_iot.py
# Pipelines de Cloud Properties
ADD python_example/cloud.properties /opt/flink/usrlib/cloud.properties
