#!/usr/bin/python

import os_client_config

nova = os_client_config.make_client('compute', cloud='amt')

def get_fixed_ip(vm):
    for net in vm.addresses:
        addr =  vm.addresses[net]
        for ip in addr:
            if ip['OS-EXT-IPS:type'] == 'fixed':
                return ip['addr']

def get_float_ip(vm):
    for net in vm.addresses:
        addr =  vm.addresses[net]
        for ip in addr:
            print ip
            if ip['OS-EXT-IPS:type'] == 'floating':
                return ip['addr']


bootstrap_host = get_float_ip(nova.servers.find(name="Bootstrap"))
master_host = []
agent_host = []

for server in nova.servers.list():
    if 'Master' in server.name:
        master_host.append(get_fixed_ip(server))
    if 'Agent' in server.name:
        agent_host.append(get_fixed_ip(server))


print bootstrap_host














 
