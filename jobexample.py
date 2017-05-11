from kubernetes import client, config
from kubernetes.client import models
from optparse import OptionParser
from git import Repo
import os.path as osp
import shutil

join = osp.join
parser = OptionParser()
parser.add_option("-k","--apikey",help="apikey")
parser.add_option("-h","--host",help="api host")
parser.add_option("-i","--image",help="container image")


(options, args) = parser.parse_args()

#config.load_kube_config(config_file=options.kubeconfig)
client.configuration.api_key['authorization'] = options.apikey
client.configuration.host = options.host
v1 = client.CoreV1Api()
v1Batch = client.BatchV1Api()

#define data structure
job = models.V1Job()
job_meta = models.V1ObjectMeta()
job_spec = models.V1JobSpec()
pod_spec_template = models.V1PodTemplateSpec()
pod_spec = models.V1PodSpec()
pod_meta = models.V1ObjectMeta()
pod_spec_container = models.V1Container()
env_var = models.V1EnvVar() 

#populate data structure
#father object
job.api_version = "batch/v1"
job.kind = "Job"

#job metadata
job_meta.name = "p1"
job.metadata = job_meta

#containers spec 172.30.129.159:5000/testjob/worker
pod_spec_container.name = "c1"
pod_spec_container.image = options.image

#job spec
pod_meta.name = "j1"
pod_spec_template.metadata = pod_meta

pod_spec.containers = [pod_spec_container]
pod_spec.restart_policy = "Never"

#set app name env var
env_var.name = "APP_FILE"
env_var.value = "worker.py"
pod_spec_container.env = [env_var]
pod_spec_template.spec = pod_spec

job_spec.template = pod_spec_template

job.spec = job_spec

#shutil.rmtree("./repotmp")

#clone repo for job definition
#cloned_repo = Repo.clone_from(url="https://github.com/sdellang/ocp-jobs-example.git",to_path="./repotmp")
#job_def = open("./repotmp/job.yaml")

v1Batch.create_namespaced_job("testjob",job)

res_job = models.V1JobStatus

res_job = v1Batch.read_namespaced_job_status(job_meta.name,"testjob",pretty=True)

print(res_job)


print("Listing pods with their IPs:")
ret = v1.list_pod_for_all_namespaces(watch=False)
for i in ret.items:
    print("%s\t%s\t%s" % (i.status.pod_ip, i.metadata.namespace, i.metadata.name))