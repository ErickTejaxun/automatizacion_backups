
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






  sudo mkdir -p /srv/nfs4/servidor01
sudo mkdir -p /srv/nfs4/servidorBD01
sudo mount --bind /home/erick/backups/May-10-2020/servidor01/ /srv/nfs4/servidor01/
sudo mount --bind /home/erick/backups/May-10-2020/servidorBD01/ /srv/nfs4/servidorBD01/



sudo vim /etc/exports 
/srv/nfs4               192.168.122.0/24(rw,sync,no_subtree_check,crossmnt,fsid=0)
/srv/nfs4/servidor01    192.168.122.181(rw,sync,no_subtree_check)
/srv/nfs4/servidorBD01  192.168.122.128(rw,sync,no_subtree_check)

/srv/nfs4               192.168.122.0/24(ro,sync,no_subtree_check,crossmnt,fsid=0)
/srv/nfs4/servidor01    192.168.122.181(ro,sync,no_subtree_check)
/srv/nfs4/servidorBD01  192.168.122.128(ro,sync,no_subtree_check)
sudo exportfs -arvf
sudo systemctl start nfs-kernel-server

sudo exportfs -v

sudo ufw allow from 192.168.122.0/24 to any port nfs
sudo ufw enable





--------------------------------->guest 
sudo apt update
sudo apt install nfs-common

sudo mkdir -p /servidorBD01
sudo mount -t nfs -o vers=4 sudo exportfs -ra
sudo mount -t nfs -o vers=4 192.168.1.49:/servidorBD01 /servidorBD01

//SQl dump
sudo mysqldump -u 'root' --all-databases --result-file= sqlfile.sql
sudo umount /servidorBD01/
