# Virtualización y escalabilidad de servidores

Este proyecto tiene como objetivo el desarrollar un sistema de automatización de backups para máquinas virutales ejecutadas a través de KVM. 
El proyecto consta de tres scripts
1. Script de snapshots a máquinas virtuales:
```bash
python3 ./snapshots_host.py
```
2. Script de snapshots a base de datos:
```bash
python3 ./snapshots_db.py
```
3. Script de snapshots a aplicación web en el servidor de frontal:
```bash
python3 ./snapshots_front_end.py
```

Para instalar las librerías necesarias:
```bash
pip install requisitos.txt
```

## Uso
El script puede ser lanzado manualmente en cada una de los servidores. 
Se recomienda el uso de crontab para poder ejecutar como damon cada uno de los scripts. 




## Licencia
[MIT](https://choosealicense.com/licenses/mit/)