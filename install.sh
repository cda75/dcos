#!/bin/bash

export ANSIBLE_HOST_KEY_CHECKING=False

ansible-playbook pre_req_install.yaml

python vm_create.py --master=1 --agent=3

#Clear known_hots file from existing host keys
while read line; do
    ssh-keygen -f "/root/.ssh/known_hosts" -R $line
    ssh-keyscan -H $line >> ~/.ssh/known_hosts
    sleep 5
done < all_ip
rm -f all_ip

echo "Waiting for nodes start up"
sleep 10

ansible-playbook docker_install.yaml

ansible-playbook bootstrap.yaml

ansible-playbook master.yaml

ansible-playbook agent.yaml


