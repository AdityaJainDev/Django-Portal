#!/bin/bash

sudo apt install kubernetes -y

sudo apt install ansible -y

ansible-galaxy collection install hetzner.hcloud

sudo apt install python3-pip -y

pip install hcloud

kubectl -n kube-system create secret generic hcloud --from-literal=token=${GITLAB_ACCESS_TOKEN}

kubectl -n kube-system create secret generic hcloud-csi --from-literal=token=${GITLAB_ACCESS_TOKEN}

kubectl apply -f  https://github.com/hetznercloud/hcloud-cloud-controller-manager/releases/latest/download/ccm.yaml #integrate your Kubernets cluster with the Hetzner Cloud API.

kubectl apply -f https://raw.githubusercontent.com/hetznercloud/csi-driver/v1.6.0/deploy/kubernetes/hcloud-csi.yml

helm repo add ingress-nginx https://kubernetes.github.io/ingress-nginx
helm repo update

echo "Please insert Domain name to create a Load-Balancer which you are willing to use the ingress-nginx for in your cluster"
read -r Domain

helm install nginx-controller ingress-nginx/ingress-nginx && kubectl annotate  --overwrite service/nginx-controller-ingress-nginx-controller "load-balancer.hetzner.cloud/location=${location}" && kubectl annotate  --overwrite service/nginx-controller-ingress-nginx-controller "load-balancer.hetzner.cloud/hostname=$Domain" && kubectl annotate --overwrite service/cert-manager "cert-manager.io/cluster-issuer=letsencrypt-prod"  -n cert-manager
