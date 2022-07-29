# Portal-Webapplication on Kubernetes

## Values

| Variable | Default | Comment |
| --- | --- | --- |
| `image.tag` | deploy | Find proper image tag in our [Docker Registry](https://git.aditsystems.de/as-crm/portal/container_registry/41) |
| `os.admin_password` | none | choose password initially |
| `instanceDomain` | none | the instance domain |
| `portal.replicas` | `1` | number of OpenSlides server pods (default is fine) |
| `clusterIssuer` | `letsencrypt-prod` | R3 Issuer from ACME |


## Initial deployment

To deploy the chart for the first time:

* create the namespace:
  ```
  kubectl create namespace foo
  ```
  Namespace recommendation: take instanceDomain, replace any non-alpha-num chars.
* install the chart:
  ```bash
  helm upgrade  --install  --namespace $KUBE_NAMESPACE --reuse-values --set image.tag=main --set instanceDomain=os.example.com portal .
  ```  

For automated installation please refer to the script setup-portal.sh [here](https://git.aditsystems.de/as-crm/portal/-/blob/deploy/kubespray/setup-portal.sh).

## Upgrades / changes

If changes need to be deployed:

```bash
helm upgrade  --install  --namespace $KUBE_NAMESPACE --reuse-values --set image.tag=deploy portal .
```

This will update the existing chart. If a new image tag is being passed, a re-deployment is triggered.
