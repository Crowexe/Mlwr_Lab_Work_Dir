import json
import os
import sys
import subprocess

def powerButton(onOff,ruta_archivo):
    with open("C:/Users/Crow9/Desktop/Mlwr_Lab_Work_Dir/Configuraciones/scripts/"+ ruta_archivo + "/configuracion.json") as config:
        datos = json.load(config)

    nameVM = datos['nameVM']
    snapshot = datos['snapshot']
    rutaUser = datos['rutaUser']
    rutaHost = datos['rutaHost']
    ip = datos['ipCmd']


    if onOff == 'on':
        subprocess.run(["VBoxManage", "snapshot", nameVM, "restore", snapshot])
        subprocess.run(["VBoxManage", "startvm", nameVM, "--type", "headless"])
    elif onOff == 'off':
        subprocess.run(["VBoxManage", "controlvm", nameVM, "poweroff"])
        subprocess.run(["VBoxManage", "snapshot", nameVM, "restore", snapshot])
    else:
        print('Debe elegir si deseas encender o apagar la maquina.')

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print('Debe elegir el tipo de maquina y si deseas encender o apagar la maquina.')
    else:
        onOff = sys.argv[1]
        ruta_archivo = sys.argv[2]

        powerButton(onOff,ruta_archivo)
