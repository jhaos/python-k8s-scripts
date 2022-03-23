#!/usr/bin/env python3.6

# Copyright (C) 2015-2020, Wazuh Inc.

from kubernetes import config
from kubernetes.client import Configuration
from kubernetes.client.rest import ApiException
from kubernetes.client.apis import core_v1_api
from kubernetes.stream import stream

DEFAULT_ENVS = ["default", "kube-node-lease", "kube-public", "kube-system", "monitoring"]



def pod_exec(v1, namespace, pod, command):


    exec_command = ['/bin/bash', '-c', command]
    response = stream(v1.connect_get_namespaced_pod_exec,
                    pod,
                    namespace,
                    command=exec_command,
                    stderr=True, stdin=False,
                    stdout=True, tty=False, _request_timeout=5)
    if not response:
        raise Exception("Timeout reached in ns: {}".format(ns))

    return response


def load_k8s_conf(key):
    config.load_kube_config("/home/centos/" + key + ".kube")
    c = Configuration()
    c.assert_hostname = False
    Configuration.set_default(c)
    v1 = core_v1_api.CoreV1Api()

    return v1


def main():


    for key in REGIONS:
        env_id = ""
        category = ""
        ns = ""
        ns_number = 15
        v1 = load_k8s_conf(key)
        managers_number = 0
        current_cluster = 0
        all_ns = v1.list_namespace().items
        command = "echo \"Executing command\""
        for ns in all_ns:
            try:
                namespace = ns.metadata.name
                ns_number = ns_number - 1
                if ns_number == 0:  ## Decorator in development
                    v1 = load_k8s_conf(key)
                    ns_number = 15

                pod_list = v1.list_namespaced_pod(namespace)

                for pod in pod_list.items:
                    current_cluster = pod_exec(v1, namespace, pod.metadata.name, command)
            except Exception as e:
                print(f"Found error: {e}")


if __name__ == '__main__':
    main()