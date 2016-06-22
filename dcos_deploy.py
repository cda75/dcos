#!/usr/bin/python

import argparse
#from ansible.playbook import PlayBook
#from  ansible.inventory import Inventory
#from ansible import callbacks
#from ansible import utils
#from  ConfigParser import SafeConfigParser
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


# Read environment vars from config file
'''
parser = SafeConfigParser()
parser.read('cloud.ini')
user =  parser.get('amt_cloud','OS_USERNAME')
url = parser.get('amt_cloud','OS_AUTH_URL')
passw = parser.get('amt_cloud','OS_PASSWORD')
tenant = parser.get('amt_cloud','OS_TENANT_NAME')

#glance = os_client_config.make_client('image', cloud='amt')
#neutron = os_client_config.make_client('network', cloud='amt')
#print type(nova)
#images =  glance.images.list()
#net_list =  neutron.list_networks()
#print "\nNeutron Net list:\n"
#for net in net_list['networks']:
#    print net['name']
'''

nova = os_client_config.make_client('compute', cloud='amt')

m_flavor_id = nova.flavors.find(name='m1.small')
a_flavor_id = nova.flavors.find(name='m1.medium')
image_id = nova.images.find(name='Ubuntu 14.04')
key_id = "mesos_key"

nova.servers.create(name='DC-OS_Master', image=image_id, flavor=m_flavor_id, key_name=key_id, min_count=m_nodes)
nova.servers.create(name='DC-OS_Agent', image=image_id, flavor=a_flavor_id, key_name=key_id, min_count=a_nodes)

# wait for server create to be complete
for server in nova.servers.list():
    while server.status == 'BUILD':
        print "Building VMs ........"
        time.sleep(5)
        server = nova.servers.get(server.id)  # refresh server
    if server.status == 'ACTIVE':
        server.add_floating_ip(get_floating_ip())





 
