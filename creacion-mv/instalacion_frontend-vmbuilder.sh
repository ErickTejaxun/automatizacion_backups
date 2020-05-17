#!/bin/bash

vmbuilder kvm ubuntu  \
	--suite precise \
	--flavour virtual \
	--arch amd64 \
	--hostname ubuntu-server-db2\
	--libvirt qemu:///system\
	--rootsize=2046 \
	--swapsize=512 \
	--user admin\
	--pass capitantrueno\
	--d prueba\
	--addpkg openssh-server\
	--mirror http://de.archive.ubuntu.com/ubuntu \ 

