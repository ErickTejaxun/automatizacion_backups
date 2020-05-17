#!/bin/bash

virt-install --connect qemu:///system  \
             	--virt-type=kvm   \
             	--name servidorDebian   \
	     		--memory 10240 \
	     		--ram 1024 \
	     		--vcpus=1 \
	     		--disk path=/var/lib/libvirt/images/servidorDebian.img,size=8 \
	     		--cdrom /var/lib/libvirt/images/debian-10.3.0-amd64-netinst.iso \
	     		--os-type linux  \
	     		--os-variant=ubuntuprecise \
	     		--graphics vnc,keymap=es \
	     		--noautoconsole   \
	     		--network network=default \
	     		--description "Debian Server  Back end " 
