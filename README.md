## Prueba carranza
Pipeline funcional para el demostrar capacidad de Flink.

##### Pasos impuestos por alfredito:
* Contruir imagen de flink con pyflink y demo.py
* Aprovisionar en minikube flink kubernetes operator
* Ejecutar prueba
* Evidenciar


##### Detalle:
* Build de imagen con pyflink y demo.py
* Adicionar repo de helm para flink operator
* Despliegue con values.yaml de flink


##### Instalación de repo para helm:
* helm repo add flink-operator-repo https://downloads.apache.org/flink/flink-kubernetes-operator-1.11.0/
* helm install flink-operator flink-operator-repo/flink-kubernetes-operator --namespace flink --create-namespace --values values.yaml

docker build --no-cache -t local-pyflink:revision .
docker build -t local-pyflink:revision .

minikube image load local-pyflink:revision

* Borrar deploy y pods
    * helm uninstall flink-operator -n kube-ope-flink 
    * kubectl delete deployment send-pod -n kube-ope-flink

* Borrar imagenes de minikube
    * minikube ssh
    * docker images
    * docker rmi local-pyflink:revision
    * exit

* python iot (send):
    * kubectl apply -f send.yaml -n flink
    * kubectl port-forward service/send-rest 8081:8081 -n kube-ope-flink
* python iot (send):
    * kubectl apply -f receptor.yaml -n kube-ope-flink
    * kubectl port-forward service/receptor-rest 8081:8081 -n kube-ope-flink

kubectl exec -it send-pod-65f66b95d-xmwhb -n kube-ope-flink -- /bin/bash
cd /opt/flink/usrlib/
python3 send_iot.py

python3 -m pip show apache-flink

python3 -m pip uninstall apache-flink -y

python3 -m pip install apache-flink==1.16.3
***

Datos importantes - Confluent:
* topico creado: 
    * Topic_name: topic-test-1
    * Partitions: 6
* key: 4INZQR6SVQ42QHQM
* secret: mUhX+eIzA9JgIuUp1RepDjzDpFoP+6pfOpTqrGg2AJV6Dt4hqghjFFKMTBSDXzZi
* output_message_format: JSON
* number_task: 1

* connector_class: DatagenSource
* connector_name: DatagenSourceConnector_0

```json
{
  "config": {
    "connector.class": "DatagenSource",
    "name": "DatagenSourceConnector_0",
    "kafka.auth.mode": "KAFKA_API_KEY",
    "kafka.api.key": "4INZQR6SVQ42QHQM",
    "kafka.api.secret": "****************************************************************",
    "kafka.topic": "topic-test-1",
    "schema.context.name": "default",
    "output.data.format": "JSON",
    "quickstart": "ORDERS",
    "max.interval": "1000",
    "tasks.max": "1",
    "value.converter.decimal.format": "BASE64",
    "value.converter.replace.null.with.default": "true",
    "value.converter.reference.subject.name.strategy": "DefaultReferenceSubjectNameStrategy",
    "value.converter.schemas.enable": "false",
    "errors.tolerance": "none",
    "value.converter.value.subject.name.strategy": "TopicNameStrategy",
    "key.converter.key.subject.name.strategy": "TopicNameStrategy",
    "value.converter.ignore.default.for.nullables": "false",
    "auto.restart.on.user.error": "true"
  }
}
```