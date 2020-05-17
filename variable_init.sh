
sudo apt-get install qemu-guest-agent
systemctl start qemu-guest-agent
systemctl enable qemu-guest-agent

PATH_BACKUPS=$HOME/backups
mkdir $PATH_BACKUPS
echo $PATH_BACKUPS



virsh snapshot-create-as servidorBD01 "servidorBD0115052020" --live

DOMAIN=servidorBD01
SNAPSHOT_NAME=$DOMAIN15052020
DISK_FILE=$PATH_BACKUPS/SNAPSHOT_NAME'/disk.qcow2'


virsh snapshot-create-as \
--domain $DOMAIN $SNAPSHOT_NAME \
--diskspec vda,file=$DISK_FILE,snapshot=external \
--memspec file=$MEM_FILE,snapshot=external \
--atomic


virsh snapshot-create-as servidor01 span-servidor01-May-17-2020 "Snapshot servidor01 programado para el día May-17-2020" \
  --diskspec vda,file=/home/erick/backups/May-17-2020/snap-servidor01.qcow2 \
  --disk-only --atomic