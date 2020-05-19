'''
Con este script  montamos el sistema de archivos desde el servidor 
y creamos la carpeta donde los guest almacenaran los archivos de los servicios que están corriendo.
'''

import sys
import os
import subprocess
from subprocess import Popen, PIPE
from datetime import date
import os.path as path
import datetime 
import paramiko


USER_BD = 'administrador'
USER_FRONT_END = 'administrador'
ID_SERVER_DB = 'servidorBD01'
ID_SERVER_FRONT= 'servidor01'
PATH_HOME_SNAPSHOT=os.environ['HOME']+'/backups'
today = date.today()
DAY =today.strftime("%b-%d-%Y")
DAY ='May-17-2020'
PATH_CURRENT_FOLDER = PATH_HOME_SNAPSHOT+'/'+DAY



def preparar_carpetas(name):
    print('Montando sistema de archivos')         

    '''Creamos las carpetas donde se almacena el snapshot'''
    if path.exists(PATH_CURRENT_FOLDER)==False:
        os.spawnlp(os.P_WAIT,'mkdir','mkdir',PATH_CURRENT_FOLDER)            

    PATH_CURRENT_FOLDER_DOMAIN = PATH_CURRENT_FOLDER+'/'+name
    if path.exists(PATH_CURRENT_FOLDER_DOMAIN)==False:
        os.spawnlp(os.P_WAIT,'mkdir','mkdir',PATH_CURRENT_FOLDER_DOMAIN)        
        os.spawnlp(os.P_WAIT,'touch','touch','ip.txt')
        os.spawnlp(os.P_WAIT,'mkdir','mkdir',PATH_CURRENT_FOLDER_DOMAIN+'/hostdata')
        os.spawnlp(os.P_WAIT,'chmod','chmod','777',PATH_CURRENT_FOLDER_DOMAIN+'/hostdata')

    if path.exists(PATH_CURRENT_FOLDER_DOMAIN+'/template')==False:
        os.spawnlp(os.P_WAIT,'mkdir','mkdir',PATH_CURRENT_FOLDER_DOMAIN+'/template') 

    '''Antes de crear el snapshot vamos a crear un archivo xml para almacenar detalles del snapshot'''
    PATH_XML_DETAIL=PATH_CURRENT_FOLDER_DOMAIN+'/template/'+name+'.xml'
    if path.exists(PATH_XML_DETAIL)==False:
        DETAIL_XML_CONT= "<domainsnapshot>\n\t<name>snap-"+name+"</name>\n\t<description>Snapshot del día "+DAY+"</description>\n</domainsnapshot>\n"
        f = open(PATH_XML_DETAIL, "w+")
        f.write(DETAIL_XML_CONT)
        f.close()
    os.spawnlp(os.P_WAIT,'mount','mount','--bind',PATH_CURRENT_FOLDER_DOMAIN,'/srv/nfs4/servidorBD01/')



'''Inicio de la ejecución del script'''
euid = os.geteuid() 
if euid != 0:
     print('Error: El script necesita ser ejecutado como root.')
     exit()
dominios = [ ID_SERVER_DB ,ID_SERVER_FRONT ]
for item in dominios:
    preparar_carpetas(item)
sys.exit(0)
