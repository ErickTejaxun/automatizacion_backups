'''Script para montaje del sistema NFS hacia el servidor host
Y copia de seguridad de la base de datos
Erick Tejaxún
'''

import sys
import os
import subprocess
from subprocess import Popen, PIPE
from datetime import date
import os.path as path
import datetime 


SERVER_PATH_DIRECTORY ='192.168.1.49:/servidor01'
CURRENT_DIRECTORY= '/servidor01/'


def copiar_base_datos():
    SERVER_PATH_DIRECTORY ='192.168.1.49:/servidor01'
    CURRENT_DIRECTORY= '/servidor01/'
    '''Primero montamos el sistema de archivos nfs'''
    os.spawnlp(os.P_WAIT,'mount','mount','-t','nfs','-o','vers=4',SERVER_PATH_DIRECTORY,CURRENT_DIRECTORY)
    if path.exists(CURRENT_DIRECTORY+'ip.txt')==False:
        print('No se ha montado el directorio remoto con nfs.')
        desmontar_sistema()
        sys.exit(0)

    '''Verificamos que la carpeta para los datos del host exista en el directorio '''
    CURRENT_DIRECTORY= CURRENT_DIRECTORY+'hostdata/'
    if path.exists(CURRENT_DIRECTORY)==False:
        os.spawnlp(os.P_WAIT,'mkdir','mkdir',CURRENT_DIRECTORY)
    
    '''Creamos la carpeta especifica para la copia de la base de datos a la hora de la ejecucion'''
    TIME =datetime.datetime.now().strftime("%b-%d-%Y-%I-%M-%p")
    DIRECTORY_FOR_HTML = CURRENT_DIRECTORY+'html'+TIME
    os.spawnlp(os.P_WAIT,'mkdir','mkdir',DIRECTORY_FOR_HTML)    

    '''Realizamos el volcado de las páǵinas del servidor web'''
    os.spawnlp(os.P_WAIT,'cp','cp','-r','/var/www/html/',DIRECTORY_FOR_HTML)    
    desmontar_sistema()

def desmontar_sistema():
    '''Desmontamos el sistema de archivos nfs'''
    os.spawnlp(os.P_WAIT,'umount','umount',CURRENT_DIRECTORY)

'''Inicio de la ejecución del script'''
euid = os.geteuid() 
if euid != 0:
     print('Error: El script necesita ser ejecutado como root.')
     sys.exit(0)
copiar_base_datos()
sys.exit(0)