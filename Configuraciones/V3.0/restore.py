import json
import os
import sys
import subprocess

def restoreVM(ruta_archivo):
    with open("C:/Users/Crow9/Desktop/Mlwr_Lab_Work_Dir/Configuraciones/scripts/"+ ruta_archivo + "/configuracion.json") as config:
        datos = json.load(config)

    nameVM = datos['nameVM']
    snapshot = datos['snapshot']
    rutaUser = datos['rutaUser']
    rutaHost = datos['rutaHost']
    ip = datos['ipCmd']

    subprocess.run(["VBoxManage", "snapshot", nameVM, "restore", snapshot])

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('Debe especificar el tipo de pruebas que deseas correr.')
    else:
        ruta_archivo = sys.argv[1]
        restoreVM(ruta_archivo)