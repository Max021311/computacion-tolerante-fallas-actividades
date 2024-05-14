#!/bin/sh

while [ true ]; do
  echo \$ kubectl get pods
  kubectl get pods
  sleep 1
done

