#!/bin/bash


PATH_BACKUPS=$HOME/backups/
DOMAIN="servidorBD01"
TIMESTAMP=`date +%s`
SNAPSHOT_NAME=$TIMESTAMP

mkdir $PATH_BACKUPS/servidorBD01
VM_FOLDER=$PATH_BACKUPS/servidorBD01/
SNAPSHOT_FOLDER="`echo $VM_FOLDER`/`echo $DOMAIN`/snapshots/`echo $TIMESTAMP`"
mkdir -p $SNAPSHOT_FOLDER

MEM_FILE="`echo $SNAPSHOT_FOLDER`/mem.qcow2"
DISK_FILE="`echo $SNAPSHOT_FOLDER`/disk.qcow2"

# Find out if running or not
STATE=`virsh dominfo $DOMAIN | grep "State" | cut -d " " -f 11`

if [ "$STATE" = "running" ]; then

  virsh snapshot-create-as \
    --domain $DOMAIN $SNAPSHOT_NAME \
    --diskspec vda,file=$DISK_FILE,snapshot=external \
    --memspec file=$MEM_FILE,snapshot=external \
    --atomic

else

  virsh snapshot-create-as \
    --domain $DOMAIN $SNAPSHOT_NAME \
    --diskspec vda,file=$DISK_FILE,snapshot=external \
    --disk-only \
    --atomic

fi