import json
import sys
import os
import subprocess
import datetime
import shutil
import io

def leer_archivo_json(ruta_archivo):
    with open("C:/Users/Crow9/Desktop/Mlwr_Lab_Work_Dir/Configuraciones/scripts/"+ ruta_archivo + "/configuracion.json") as config:
        datos = json.load(config)

    nameVM = datos['nameVM']
    snapshot = datos['snapshot']
    rutaUser = datos['rutaUser']
    rutaHost = datos['rutaHost']
    ip = datos['ipCmd']

    with open(rutaHost + "/Mlwr_Lab_Work_Dir/Configuraciones/scripts/"+ ruta_archivo + "/dataset.json") as dataset:
        datos = json.load(dataset)
  
    mwUrl = datos['malware']['url']
    mwRuta = datos['malware']['ruta']
    pruebas = datos['pruebas']
    estaticas = pruebas[0]['estaticas']
    dinamicas = pruebas[1]['dinamicas']

    # Acceder a los valores dentro del diccionario 'estaticas'
    fileTest = estaticas['file']
    exiftool = estaticas['exiftool']
    md5 = estaticas['MD5']
    sha1 = estaticas['SHA1']
    sha256 = estaticas['SHA256']

    # Acceder a los valores dentro del diccionario 'dinamicas'
    objdump = dinamicas['objdump']
    strace = dinamicas['strace']    

    # Obtener el nombre del archivo
    def get_filename_from_path(mw_ruta):
        mw_name = os.path.basename(mw_ruta)
        return mw_name 

    #subprocess.run(["VBoxManage", "snapshot", nameVM, "restore", snapshot])
    #subprocess.run(["VBoxManage", "startvm", nameVM, "--type", "headless"])

    # Obtener la fecha y hora actual
    date = datetime.datetime.now().strftime('%Y%m%d-%H%M%S')

    print(f'{mwRuta} es un archivo')
    print(get_filename_from_path(mwRuta))
    mw_name = get_filename_from_path(mwRuta)

    # Envía el malware al laboratorio
    subprocess.run(["SCP", mwRuta, "analista@" + ip + ":" + rutaUser])
    print("Ejecutando file")
    output = subprocess.check_output(["ssh", "analista@" + ip, "file", rutaUser + "/" + mw_name], shell=True)
    buffer = io.StringIO(output.decode())
    with open('file-'+date+'.txt', 'w') as archivo:
        archivo.write(buffer.getvalue())
    archivo.close()

    print("Ejecutando exiftool")
    output = subprocess.check_output(["ssh", "analista@" + ip, "exiftool", rutaUser + "/" + mw_name],shell=True)
    buffer = io.StringIO(output.decode())
    with open('exiftool-'+date+'.txt', 'w') as archivo:
        archivo.write(buffer.getvalue())
    archivo.close()

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('Debe especificar el tipo de pruebas que deseas correr.')
    else:
        ruta_archivo = sys.argv[1]
        leer_archivo_json(ruta_archivo)
        #subprocess.run(["VBoxManage", "controlvm", nameVM, "poweroff"])
        #subprocess.run(["VBoxManage", "snapshot", nameVM, "restore", snapshot])