#!/usr/bin/python

import os_client_config

nova = os_client_config.make_client('compute', cloud='amt')

def get_fixed_ip(vm):
    for net in vm.addresses:
        addr =  vm.addresses[net]
        for ip in addr:
            if ip['OS-EXT-IPS:type'] == 'fixed':
                return ip['addr']


bootstrap_host = get_fixed_ip(nova.servers.find(name="Bootstrap"))
master_host = []
agent_host = []

for server in nova.servers.list():
    if 'Master' in server.name:
        master_host.append(get_fixed_ip(server))
    if 'Agent' in server.name:
        agent_host.append(get_fixed_ip(server))


print bootstrap_host
print master_host
print agent_host

with open("/etc/ansible/hosts", "a") as f:
    f.write('#BEGIN DCOS\n')
    f.write('[dcos_bootstrap]\n')
    f.write("%s\n" %bootstrap_host)
    f.write('[dcos_agent]\n')
    for host in agent_host:
        f.write("%s\n" %host)
    f.write('[dcos_master]\n')
    for host in master_host:
        f.write("%s\n" %host)
    f.write('#END DCOS\n')















 
