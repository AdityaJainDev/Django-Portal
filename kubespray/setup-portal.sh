#!/bin/bash

helm repo add jetstack https://charts.jetstack.io
helm repo update

helm install \
cert-manager jetstack/cert-manager \
--namespace cert-manager \
--create-namespace \
--set installCRDs=true

echo "Please insert subdomain or a domain name for portal"
read -r Domain
echo "Please insert the namespace for Installation of portal with lower case alphanumeric characters and/or must start and end with an alphanumeric character"
read -r namespace
KUBECONFIG=./inventory/Portal/${clustername}/artifacts/admin.conf kubectl create namespace "$namespace"; 
echo "Please insert the Image for deploying on portal/ images available: deploy, main, build, latest, 14-container-is-not-starting-in-k8s"
read -r imagetag

kubectl apply -f prod_issuer.yaml #Create the clusterIssuer which is used from cert-manger k8s resource to automatically issue certificates. https://cert-manager.io/docs/configuration/acme/

cd ./helmcharts/Portal/ || exit;
KUBECONFIG=./../../inventory/Portal//${clustername}/artifacts/admin.conf helm  upgrade --install --namespace "$namespace" --set image.tag="$imagetag" --set instanceDomain="$Domain" portal .
echo instanceDomain="$Domain"
