## You need to execute with the user that has kube config to get the configuration

from kubernetes import config
from kubernetes.client import Configuration
from kubernetes.client.rest import ApiException
from kubernetes.client.apis import core_v1_api
from kubernetes.stream import stream
import urllib3
import json
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

ignored_namespaces = [
    "default",
    "kube-public",
    "kube-system",
    "kube-node-lease",
]
def main():
    config.load_kube_config()
    c = Configuration()
    c.assert_hostname = False
    Configuration.set_default(c)
    core_v1 = core_v1_api.CoreV1Api()
    namespaces = core_v1.list_namespace()

    for ns in namespaces.items:
        if ns.metadata.name not in ignored_namespaces:
            print(ns)
    exit(0)



if __name__ == '__main__':
    main()
