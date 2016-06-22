#!/usr/bin/python

import argparse
import os_client_config
import time

parser = argparse.ArgumentParser(description='Deploying DC/OS Mezosphere cluster')
parser.add_argument("--master", type=int, default=1)
parser.add_argument("--agent", type=int, default=3)
parser.add_argument("--distr", type=str, default='CentOS')
args = parser.parse_args()
m_nodes = args.master
a_nodes = args.agent
node_distr = args.distr


def get_floating_ip():
    float_ip_pool = nova.floating_ips.list()
    if float_ip_pool:
        for fip in float_ip_pool:
            if fip.instance_id == None:
                print "Attaching floating IP ....."
                return fip.ip
        print 'Allocating new Floating ip to Project'
        try:
            fip = nova.floating_ips.create()
            print fip.ip
            return fip.ip
        except novaclient.exceptions.Forbidden:
            print " No more Floating IP available for the Project"

    else:
        print 'Allocating new Floating ip to Project'
        try:
            fip = nova.floating_ips.create()
            print fip.ip
            return fip.ip
        except novaclient.exceptions.Forbidden:
            print " No more Floating IP available for the Project"


def get_fixed_ip(vm):
    for net in vm.addresses:
        addr =  vm.addresses[net]
        for ip in addr:
            if ip['OS-EXT-IPS:type'] == 'fixed':
                return ip['addr']


# Read environment vars from config file
'''
from  ConfigParser import SafeConfigParser
parser = SafeConfigParser()
parser.read('cloud.ini')
user =  parser.get('amt_cloud','OS_USERNAME')
url = parser.get('amt_cloud','OS_AUTH_URL')
passw = parser.get('amt_cloud','OS_PASSWORD')
tenant = parser.get('amt_cloud','OS_TENANT_NAME')
'''

nova = os_client_config.make_client('compute', cloud='amt')

m_flavor_id = nova.flavors.find(name='m1.small')
a_flavor_id = nova.flavors.find(name='m1.medium')

for image in nova.images.list():
    if node_distr.lower() in image.name.lower():
        image_id = image.id

if nova.keypairs.list():
    key_id = nova.keypairs.list()[0].name
else:
    key_id = nova.keypairs.create(name='key1').name

# Creating VMs
nova.servers.create(name='Master', image=image_id, flavor=m_flavor_id, key_name=key_id, min_count=m_nodes)
nova.servers.create(name='Agent', image=image_id, flavor=a_flavor_id, key_name=key_id, min_count=a_nodes)
bootstrap = nova.servers.create(name='Bootstrap', meta={'hostname': 'bootstrap'}, image=image_id, flavor=m_flavor_id, key_name=key_id)

# wait for server create to be complete and attach Floating IP to it
for server in nova.servers.list():
    while server.status == 'BUILD':
        print "Building VMs ........"
        time.sleep(5)
        server = nova.servers.get(server.id)  # refresh server
    if server.status == 'ACTIVE':
        server.add_floating_ip(get_floating_ip())

bootstrap_host = get_fixed_ip(nova.servers.find(name="Bootstrap"))
master_host = []
agent_host = []

for server in nova.servers.list():
    if 'Master' in server.name:
        master_host.append(get_fixed_ip(server))
    if 'Agent' in server.name:
        agent_host.append(get_fixed_ip(server))

#Update Ansible hosts file
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






 