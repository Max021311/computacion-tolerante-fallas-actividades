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

5. Edit the manifest.yaml if needed to use the required image. In this case is `jose9348/node-app:1.0`

6. Apply the content of the manifest.

```sh
kubectl apply -f manifest.yaml
```

7. Init the Minikube tunnel that allow connections to the Ingress.
```sh
minikube tunnel
```

8. Make many request to `http://127.0.0.1/ok` to check if the load balancer change the service instances used.
