# How to test Kubernetes locally

## Build and upload server image to docker hub

Replace `jose9348` with your docker hub user.

1. Build
```sh
docker build -t jose9348/node-app:1.0
```

2. Upload
```sh
docker push jose9348/node-app:1.0
```

## Install and setup Minikube

1. Install minikube. [https://minikube.sigs.k8s.io/docs/start/](See).

2. Start minikube
```sh
minikube start
```

3. Test Minikube
```sh
minikube kubectl -- get po -A
```

4. Enable Ingress in Minikube

```sh
minikube addons enable ingress
```

5. Init the Minikube tunnel that allow connections to the Ingress.
```sh
minikube tunnel
```
6. Install Istio inside the cluster
```bash
istioctl install --set profile=demo -y
```

7. Enable the injection of Istio
```bash
kubectl label namespace default istio-injection=enabled
```

8. Install Kiali dashboard inside the cluster
```bash
kubectl apply -f https://raw.githubusercontent.com/istio/istio/release-1.21/samples/addons/kiali.yaml
```

9. Install Prometheus inside the cluster.

```bash
kubectl apply -f https://raw.githubusercontent.com/istio/istio/release-1.21/samples/addons/prometheus.yaml

10. Open Kiali dashboard
```bash
istioctl dashboard kiali
```

11. Edit the manifest.yaml if needed to use the required image. In this case is `jose9348/node-app:1.0`

12. Apply the content of the manifest.
```bash
kubectl apply -f manifest.yaml
```

12. Make a request to `http://127.0.0.1/api/v1/ok` and `http://127.0.0.1/api/v2/ok` to check if the Istio gateway works.
