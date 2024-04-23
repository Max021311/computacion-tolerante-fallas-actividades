# How to run

This command executes two servers instances of the same image in different ports and one instance of nginx that balance the queries to this this two servers.
```sh
docker compose up
```

## How to test

If you run the below command you can see in the logs of docker how each query is redirected to a one of the servers specified in nginx.conf.
```sh
curl http://localhost:3000/ok
```
