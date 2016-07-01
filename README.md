# dcos
Deploying DC/OS cluster on OPenStack
Based on Centos 7 distro
OpenStack credentials are in clouds.yaml file. Based on os-client-config library
OpenStack should use password authentication/
Script VM_CREATE.PY creates --master and --agent nodes
Use vm_create.py --master <number of master nodes> --agent <number of agent nodes>
All other scripts based on Ansible playbioks
on Ansible host should be installed openstack-python client and Shade.
