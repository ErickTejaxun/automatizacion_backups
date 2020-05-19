from __future__ import print_function
import libvirt
import sys
import os
import subprocess
from subprocess import Popen, PIPE
from datetime import date
import time
import datetime
import os.path as path



#/var/lib/libvirt/images/servidor01.qcow2
#/var/lib/libvirt/images/servidorBD01.img

USER_BD = 'administrador'
USER_FRONT_END = 'administrador'
PASSWORD = 'capitantrueno'
ID_SERVER_DB = 'servidorBD01'
ID_SERVER_FRONT= 'servidor01'
PATH_HOME_SNAPSHOT=os.environ['HOME']+'/backups'
today = date.today()
DAY =today.strftime("%b-%d-%Y")
PATH_CURRENT_FOLDER = PATH_HOME_SNAPSHOT+'/'+DAY
PATH_VIRSH_QEMU_SNAPSHOTS= '/var/lib/libvirt/qemu/snapshot/'

def show_information_domain(domain, name):
    print('------------------------------------------')        
    if domain == None:
        print('Error: no existe el dominio '+name)        
    else:
        id = domain.ID()
        if id == -1:
            print('El dominio '+name+ ' no está en ejecución. No cuenta con ID')
        else:
            print('El id del dominio ' + name + ' es ' + str(id) + '. Ejecuntando ' + domain.OSType())  
        flag = domain.hasCurrentSnapshot()
        print('El valor del actual snapshot de '+name +' es flag is ' + str(flag)) 
        flag = dom_servidor_db.hasManagedSaveImage()
        print('El valor del administrador de snapshot es ' + str(flag))

        flag = domain.isActive()
        if flag == True:
            print('El dominio está activo')
            return True
        else:
            print('El dominio está inactivo')
            return False

    

def tomar_snapshot(domain,name):
    print('Comenzando backup')       
    print('Creando carpeta')  

    '''Eliminamos el snapshot por si existe
    PATH_XML_SNAPSHOT= PATH_VIRSH_QEMU_SNAPSHOTS+name+'/'+name+DAY+'.xml'
    if path.exists(PATH_XML_SNAPSHOT):
        os.spawnlp(os.P_WAIT, 'rm','rm',PATH_XML_SNAPSHOT)
    '''

    '''Creamos las carpetas donde se almacena el snapshot'''
    if path.exists(PATH_CURRENT_FOLDER)==False:
        os.spawnlp(os.P_WAIT,'mkdir','mkdir',PATH_CURRENT_FOLDER)            

    PATH_CURRENT_FOLDER_DOMAIN = PATH_CURRENT_FOLDER+'/'+name
    if path.exists(PATH_CURRENT_FOLDER_DOMAIN)==False:
        os.spawnlp(os.P_WAIT,'mkdir','mkdir',PATH_CURRENT_FOLDER_DOMAIN)

    if path.exists(PATH_CURRENT_FOLDER_DOMAIN+'/template')==False:
        os.spawnlp(os.P_WAIT,'mkdir','mkdir',PATH_CURRENT_FOLDER_DOMAIN+'/template') 

    '''Antes de crear el snapshot vamos a crear un archivo xml para almacenar detalles del snapshot'''
    PATH_XML_DETAIL=PATH_CURRENT_FOLDER_DOMAIN+'/template/'+name+'.xml'
    if path.exists(PATH_XML_DETAIL)==False:
        DETAIL_XML_CONT= "<domainsnapshot>\n\t<name>snap-"+name+"</name>\n\t<description>Snapshot del día "+DAY+"</description>\n</domainsnapshot>\n"
        f = open(PATH_XML_DETAIL, "w+")
        f.write(DETAIL_XML_CONT)
        f.close()

    '''Copiamos la configuración de la máquina virtual'''
    os.spawnlp(os.P_WAIT,'cp','cp','/etc/libvirt/qemu/'+name+'.xml',PATH_CURRENT_FOLDER_DOMAIN+'/template/'+name+'.xml')
    os.spawnlp(os.P_WAIT,'sed','sed', '-i', '/uuid/d', PATH_CURRENT_FOLDER_DOMAIN+'/template/'+name+'.xml')
    os.spawnlp(os.P_WAIT,'sed','sed', '-i', '/mac address/d', PATH_CURRENT_FOLDER_DOMAIN+'/template/'+name+'.xml')    


    '''Creamos el snapshot en modo externo'''
    os.spawnlp(os.P_WAIT, 'virsh', 'virsh', 'snapshot-create-as', '--domain',name,name+DAY,"--diskspec","hda,file="+PATH_CURRENT_FOLDER_DOMAIN+"/template/disk.qcow2","--disk-only","--atomic")
    

    '''Creamos los snapshot de memoria y disco duro '''
    #os.spawnlp(os.P_WAIT, 'virsh', 'virsh', 'snapshot-create-as', '--domain',name,name+DAY,"--diskspec","vda,file="+PATH_CURRENT_FOLDER_DOMAIN+"/disk.qcow2","snapshot=external","--memspec","file="+PATH_CURRENT_FOLDER_DOMAIN+"/mem.qcow2,snapshot=external","--atomic")
    
    '''Creamos snapshot de la configuración de la máquina virtual'''    
    #if path.exists(PATH_VIRSH_QEMU_SNAPSHOTS+name+'/'+name+DAY+'.xml'):
    #    os.spawnlp(os.P_WAIT, 'mv','mv',PATH_VIRSH_QEMU_SNAPSHOTS+name+'/'+name+DAY+'.xml',PATH_CURRENT_FOLDER_DOMAIN)


def eliminar_snapshot(dominios, max):
    print('Eliminando snapshot')
    #Contamos el número de snapshot hay
    num_snapshot = len(os.listdir(PATH_HOME_SNAPSHOT))
    if num_snapshot>max:
        print('Es necesario eliminar backups, existen '+str(num_snapshot)+' snapshots.')
        today = datetime.datetime.today()
        DD = datetime.timedelta(days=max)
        LAST_DAY = today - DD
        LAST_DAY =LAST_DAY.strftime("%b-%d-%Y")
        print('Se eliminará el snapshot del día '+LAST_DAY)
        
        for item in dominios:            
            '''virsh snapshot-delete servidor01 --metadata servidor01May-17-2020'''
            print(item[1])
            #Eliminamos el backup del qemu
            os.spawnlp(os.P_WAIT,'virsh','virsh','snapshot-delete',item[1],'--metadata',item[1]+LAST_DAY)
            #Eliminamos los archivos asociados.
            os.spawnlp(os.P_WAIT,'rm','rm','-r',PATH_HOME_SNAPSHOT+'/'+LAST_DAY)



'''Inicio de la ejecución del script'''
euid = os.geteuid() 
if euid != 0:
     print('Error: El script necesita ser ejecutado como root.')
     exit()
try:
    conn = libvirt.open('qemu:///system')
except libvirt.libvirtError:
    print('Fallo al conectarse con el hipervisor.')
    sys.exit(1)

try:
    dom_servidor_db = conn.lookupByName(ID_SERVER_DB)          #Servidor DB
    dom_servidor_front_end = conn.lookupByName(ID_SERVER_FRONT) #Servidor Front end
    dom_servidor_windows = conn.lookupByName('win10')
except libvirt.libvirtError:
    print('Error al buscar los dominios')
    sys.exit(1)


print('El sistema de virtualización del de tipo: ', conn.getType())
print('Carpeta actual : \t'+PATH_CURRENT_FOLDER)
dominios = [ [dom_servidor_db,ID_SERVER_DB],[dom_servidor_front_end,ID_SERVER_FRONT]]


'''Información de los host que nos interesan'''
for item in dominios:
    if(show_information_domain(item[0],item[1])):
        tomar_snapshot(item[0],item[1])
eliminar_snapshot(dominios,7)

conn.close()
sys.exit(0)


