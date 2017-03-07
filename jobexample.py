from kubernetes import client, config
from optparse import OptionParser
from git import Repo

parser = OptionParser()
parser.add_option("-k","--kubeconfig",help="kubeconfig file")

(options, args) = parser.parse_args()

print "kubeconfig "+options.kubeconfig

config.load_kube_config(config_file=options.kubeconfig)

v1 = client.CoreV1Api()
v1Batch = client.BatchV1Api()

#clone repo for job definition
cloned_repo = Repo.clone("https://github.com/sdellang/ocp-jobs-example.git","./repotmp")
job_def = open("./repotmp/job.yaml")

v1Batch.create_namespaced_job("testjob",job_def)


print("Listing pods with their IPs:")
ret = v1.list_pod_for_all_namespaces(watch=False)
for i in ret.items:
    print("%s\t%s\t%s" % (i.status.pod_ip, i.metadata.namespace, i.metadata.name))