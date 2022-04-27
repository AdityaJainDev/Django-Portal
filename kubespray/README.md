# Deploy a Production Ready Kubernetes Cluster

![Kubernetes Logo](https://raw.githubusercontent.com/kubernetes-sigs/kubespray/master/docs/img/kubernetes-logo.png)

If you have questions, check the documentation at [kubespray.io](https://kubespray.io) and join us on the [kubernetes slack](https://kubernetes.slack.com), channel **\#kubespray**.
You can get your invite [here](http://slack.k8s.io/)


1. first create working environment and change to the directory you want to import kubespray manifests to:  
`mkdir -p ~/git/kubespray_workspace`  
 `cd kubespray_workspace/`
2. Install the latest release first then download the package [here](https://github.com/kubernetes-sigs/kubespray/releases),  
 unpack then the Archive file.  
 `wget https://github.com/kubernetes-sigs/kubespray/archive/refs/tags/<release-Nr>.tar.gz`  
`tar xfvz v2.17.1.tar.gz`

3. install dependencies for running Kubespray with Ansible on the Management server:  
`find -name requirements.txt`  
`pip3 install -r requirements.txt`

4. Create new cluster configuration:  
`cp -rfp inventory/sample inventory/openslides`  
5. Made kubespray generate a kubeconfig file on the End-User used to run Kubespray by setting **kubeconfig_localhost** to **true** in **inventory/openslides<oder as-crm>/production<or staging>group_vars/k8s_cluster/k8s_cluster.yml**. This file will later be used to configure kubectl to access the cluster:  
```
# Make a copy of kubeconfig on the host that runs Ansible in {{ inventory_dir }}/artifacts
kubeconfig_localhost: true
# Download kubectl onto the host that runs Ansible in {{ bin_dir }}
kubectl_localhost: true
```
6. Set afterwards cloud_provider value to external in the inventory file *group_vars/all/all.yml* for using hcloud provider:
  ```
## There are some changes specific to the cloud providers
  ## for instance we need to encapsulate packets with some network plugins
  ## If set the possible values are either 'gce', 'aws', 'azure', 'openstack', 'vsphere', 'oci', or 'external'
  ## When openstack is used make sure to source in the openstack credentials
  ## like you would do when using openstack-client before starting the playbook.
  cloud_provider: external
```
7. For static inventory use:
```
declare -a IPS=(1.2.3.4 1.2.3.4 1.2.3.4 etc...)
```  
and then hit:    
`CONFIG_FILE=inventory/openslides/hosts.yaml python3 contrib/inventory_builder/inventory.py ${IPS[@]}`  
, Or execute the following CLI when hostname mussn't be *node1, node2* etc.:  
`CONFIG_FILE=inventory/openslides/hosts.yaml python3 contrib/inventory_builder/inventory.py controller-1,<IP> worker-2,<IP> worker-1,<IP> worker-3,<IP>`  

8. Run the following command to provision/create K8s Cluster Using Ansible Playbook:  
`ansible-playbook -i ./inventory/openslides/production/hosts.yaml ./cluster.yml -e ansible_user=root`    

    **If you are provisionenig staging clusters take the path inventory/openslides/staging/hosts.yaml**  
    *you can use for staging the kubectl.sh cli instead of kubectl which ist located in inventory/openslides/staging/artifacts/kubectl.sh*  
    *To change between different clusters use the command line* **export KUBECONFIG=./inventory/openslides/staging/artifacts/admin.conf**  
    *To verify the cluster via* **kubectl config view -o jsonpath='{"Cluster name\tServer\n"}{range .clusters[*]}{.name}{"\t"}{.cluster.server}{"\n"}{end}'**  

    ***(Please be aware if you are using this command for connecting to nodes with authentication methods such as username or ssh-key privileges. It is recommended to parse the parameter -e ansible_user=root assuming the target node has root as username)***  

    **If the names of created servers via terraform in the cloud console are unlike that ones in the inventory you will not be able to get services in clusters like ingress-nginx running due to taint issues**  
***Warning  FailedScheduling  3s (x4 over 2m25s)  default-scheduler  0/4 nodes are available: 4 node(s) had taint {node.cloudprovider.kubernetes.io/uninitialized: false}, that the pod didn't tolerate.***  
*To solve that you have to untaint the events and pods as described* [here](https://pet2cattle.com/2021/09/k8s-node-untaint)  

9. use the following command to get more debugging output:  
`ansible -m ping all -vvvv`  

10. To (Optional) Reset the clusters if there are any errors:  
`ansible-playbook -v -i  inventory/openslides/production/hosts.yaml reset.yml --flush-cacheasd`  

11. To use Hetzner Cloud dynamic inventroty. create a file with hcloud.yml or .yaml in your ansible cluster inventory.  
[hcloud](https://docs.ansible.com/ansible/latest/collections/hetzner/hcloud/hcloud_inventory.html#hetzner-hcloud-hcloud-ansible-dynamic-inventory-plugin-for-the-hetzner-cloud).  

12. Verifying the inventory: You can use the ansible-inventory CLI command to display the inventory as Ansible sees it:  
`ansible-inventory -i ./inventory/openslides/production/hosts.yaml --list`  

13.  Activate the Kube-Admin-configuration on your local machine with the following command:  
`cp ./inventory/openslides/artifacts/production/admin.conf /home/$USER/.kube/config`  

14. Create ingress-nginx controller and Install it Using Script setup-k8s.sh and then setup-openslides.sh for openslides website with https    
`GITLAB_ACCESS_TOKEN=(your created hetzner cloud console token) location=(the location of the LB service) bash setup-k8s.sh`  
    For openslides run:  
    `clustername=(staging or production) bash setup-openslides.sh`  

   E.g **GITLAB_ACCESS_TOKEN=0cOSNCxxxxxxx location=fsn1 bash setup-k8s.sh**    
       For Staging Cluster use the same command with location in hel1 and environment variable KUBECONFIG  
   E.g **KUBECONFIG=./inventory/openslides/staging/artifacts/admin.conf  GITLAB_ACCESS_TOKEN=hFOcxxxxxxx location=hel1 bash setup-k8s.sh**
##### Note:  
- In order the scripts should work you have to clone and fetch the repository in the folder in **helmcharts/** for directory __openslides-chart_ [here](https://git.aditsystems.de/openslides/openslides-chart)  
- If you are not in case of redirecting to https or using cert-manager delete then the parameter **--set clusterIssuer=letsencrypt-prod** from setup-openslides.sh .  
- Create for each Cloud console project a separate Token to use them when previous scripts.  
- For installing and setting up prometheus on your cluster please refer to [monitoring](https://git.aditsystems.de/openslides/Monitoring/-/tree/main)  

15. Check the ingress and pods are runinng with e.g. **kubectl get all -n default**  
since the ingress will be installed in a default namespace if that is not defined in helm. 

16. Check the created openslide app is working via e.g. **kubectl get all -n <namespace of the app>**

17. To delete the openslide app use e.g.: **helm uninstall openslides --namespace test1asservertestnet**

18. To delete the ingress-nginx Instanz use the command:
```helm uninstall nginx-controller```


Error Issues:  
- If you get the error:   
`original message: Unable to create local directories(/home/***/git/kubespray_workspace/kubespray-*/inventory/mycluster/credentials): [Errno 13] Permission denied: b'/home/siamand/git/kubespray_workspace/kubespray-2.17.1/inventory/mycluster/credentials'"}`  
Change the prompted file privileges as the following:  
`sudo chmod 744 mycluster/hosts.yaml`  
