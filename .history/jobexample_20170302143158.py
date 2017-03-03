from kubernetes import client, config

config.load_kube_config(config_file="/Users/samuele/Documents/Personal/admin.kubeconfig")

v1=client.CoreV1Api()
v1Batch=client.BatchV1Api()

job = V1Job() 
print("Listing pods with their IPs:")
ret = v1.list_pod_for_all_namespaces(watch=False)
ret = v1.
for i in ret.items:
    print("%s\t%s\t%s" % (i.status.pod_ip, i.metadata.namespace, i.metadata.name))