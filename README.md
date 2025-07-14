# Examen Sustitutorio - Desarrollo de Software
## Estudiante: `Luna Jaramillo, Christian Giovanni`
## Link del repositorio: [ES_DS-20211374B](https://github.com/Chriss5-2/ES_DS-20211374B)

### Actividad 4: Scheduler Plugin con Mediator

Para esta parte de la actividad, reciclé el servidor HTTP que se creó para la PC5 del siguiente link [app](https://github.com/grupo10-CC3S2/Proyecto7-PC4/tree/main/app) y los pods que levantaban este servicio y se encuentran en [k8s](https://github.com/grupo10-CC3S2/Proyecto7-PC4/tree/main/k8s) para así al levantarlos, poder usar el script [pipeline.sh](scripts\pipeline.sh) que lo que hará será recolectar las métricas de los pods y convertirlos guardarlos en un archivo csv `metric.csv`

#### Ejecución

Iniciamos Minikube
```bash
minikube start --driver=docker
```
Apuntamos a Minikube
```bash
eval "$(minikube -p minikube docker-env --shell bash)
```
Para ejecutar este script, lo primero que se tiene es instalar metrics-server

```bash
kubectl apply -f https://github.com/kubernetes-sigs/metrics-server/releases/latest/download/components.yaml
```

Si verificamos eso, guardamos el nombre del pods, y editaremos su archivo

```bash
kubectl edit deployment metrics-server -n kube-system
```
Esto nos abrirá un editor, y cuando haga esto, buscamos lo siguiente:
```bash
containers:
    - args:
        - --cert-dir=/tmp
        - --secure-port=10250
        - --kubelet-preferred-address-types=InternalIP,ExternalIP,Hostname
        - --kubelet-use-node-status-port
        - --metric-resolution=15s
```
Cuando encontremos eso, lo que haremos será agregar la siguiente línea
```bash
        - --kubelet-insecure-tls
```
**Ojo** Tener cuidado con los espacios

Luego de tener instalado, levantamos los servicios

```bash
docker build -t timeserver:v5 app
```

Desplegamos los pods
```bash
kubectl apply -f k8s/
```

Y luego para verificar el servicios, lo exponemos localmente con
```bash
minikube service timeserver
```

Esperamos unos segundos, y procedemos a ejecutar el script desde la carpeta raíz

```bash
bash scripts/pipeline.sh
```

Y este nos creará una carpeta `metrics` con un archivo `metric.csv` el cuál tendrá las métricas recolectadas de todos los pods

Ahora para aplicar la `Transformación` se crea el scripts [plugin.py](scripts\plugin.py) el cuál nos genera un archivo json `metrics.json` con las métricas recogidas, y lo que se tendría que implementar, sería que [pipeline.sh](scripts\pipeline.sh) lea ese archivo generado por plugin.py y lo convierta a `metrics.csv` pero por ahora ya que el script [pipeline.sh](scripts\pipeline.sh) crea el archivo `metrics.csv` con las métricas, no es necesario su lectura