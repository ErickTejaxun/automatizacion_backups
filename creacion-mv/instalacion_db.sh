#!/bin/bash

virt-install --connect qemu:///system  \
             	--virt-type=kvm   \
             	--name servidorBD01   \
	     		--memory 10240 \
	     		--ram 1024 \
	     		--vcpus=1 \
	     		--disk path=/var/lib/libvirt/images/servidorBD01.img,size=14 \
	     		--cdrom /var/lib/libvirt/images/ubuntu-18.04.4-live-server-amd64.iso \
	     		--os-type linux  \
	     		--os-variant=ubuntuprecise \
	     		--graphics vnc,keymap=es \
	     		--noautoconsole   \
	     		--network network=default \
	     		--description "Ubuntu 18.04 Server BD" 
