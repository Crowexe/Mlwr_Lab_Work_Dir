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

    # Imprimir los valores asignados a las variables
    print(nameVM, snapshot, rutaUser, rutaHost, ip)
    print(mwUrl, mwRuta,fileTest,exiftool, md5,sha1,objdump,strace)

    # Obtener el nombre del archivo
    def get_filename_from_path(mw_ruta):
        mw_name = os.path.basename(mw_ruta)
        return mw_name 

    #subprocess.run(["VBoxManage", "snapshot", nameVM, "restore", snapshot])
    #subprocess.run(["VBoxManage", "startvm", nameVM, "--type", "headless"])

    # Obtener la fecha y hora actual
    date = datetime.datetime.now().strftime('%Y%m%d-%H%M%S')

    # Crear la carpeta de experimentos
    experimentosDir = os.path.join(rutaHost+ '/Mlwr_Lab_Work_Dir/Experimentos/')
    eid = len(os.listdir(experimentosDir)) + 1
    new_experiment_dir = os.path.join(experimentosDir + str(eid))
    os.mkdir(new_experiment_dir)

    # Hacer las pruebas dependiendo del input del malware
    if os.path.isdir(mwRuta):
        print(f'{mwRuta} es una carpeta')
        malwares = os.listdir(mwRuta)

        for malware in malwares:
            print("Procesando archivo: " + malware)

            # Envía el malware al laboratorio 
            subprocess.run(["SCP", mwRuta + "/" + malware, "analista@" + ip + ":" + rutaUser])
            
            muestraDir = os.path.join(rutaHost+ '/Mlwr_Lab_Work_Dir/Experimentos/'+ str(eid)+ '/')
            sid = len(os.listdir(muestraDir)) + 1
            new_muestra_dir = os.path.join(muestraDir + str(sid))
            os.mkdir(new_muestra_dir)
            

            # Aplicamos las pruebas seleccionadas en el JSON
            if fileTest == 'true':
                print("Ejecutando file")
                output = subprocess.check_output(["ssh", "analista@" + ip, "file", rutaUser + "/" + malware], shell=True)
                buffer = io.StringIO(output.decode())
                with open(rutaHost+'/Mlwr_Lab_Work_Dir/Experimentos/'+str(eid)+'/'+str(sid)+'/file-'+date+'.txt', 'w') as archivo:
                    archivo.write(buffer.getvalue())
                archivo.close()

            if exiftool == 'true':
                print("Ejecutando exiftool")
                output = subprocess.check_output(["ssh", "analista@" + ip, "exiftool", rutaUser + "/" + malware], shell=True)
                buffer = io.StringIO(output.decode())
                with open(rutaHost+'/Mlwr_Lab_Work_Dir/Experimentos/'+str(eid)+'/'+str(sid)+'/exiftool-'+date+'.txt', 'w') as archivo:
                    archivo.write(buffer.getvalue())
                archivo.close()

            if md5 == 'true':
                print('Ejecuando MD5')
                output = subprocess.check_output(['ssh', 'analista@' + ip, 'md5sum', rutaUser + "/" + malware], shell=True)
                buffer = io.StringIO(output.decode())
                with open(rutaHost+'/Mlwr_Lab_Work_Dir/Experimentos/'+str(eid)+'/'+str(sid)+'/md5-'+date+'.txt', 'w') as archivo:
                    archivo.write(buffer.getvalue())
                archivo.close()

            if sha1 == 'true':
                print('Ejecutando SHA1')
                output = subprocess.check_output(['ssh', 'analista@' + ip, 'sha1sum', rutaUser + "/" + malware], shell=True)
                buffer = io.StringIO(output.decode())
                with open(rutaHost+'/Mlwr_Lab_Work_Dir/Experimentos/'+str(eid)+'/'+str(sid)+'/sha1-'+date+'.txt', 'w') as archivo:
                    archivo.write(buffer.getvalue())
                archivo.close()

            if sha256 == 'true':
                print('Ejecutando SHA256')
                output = subprocess.check_output(['ssh', 'analista@' + ip, 'sha256sum', rutaUser + '/' + malware], shell=True)
                buffer = io.StringIO(output.decode())
                with open(rutaHost+'/Mlwr_Lab_Work_Dir/Experimentos/'+str(eid)+'/'+str(sid)+'/sha256-'+date+'.txt', 'w') as archivo:
                    archivo.write(buffer.getvalue())
                archivo.close()
            
            if objdump == 'true':
                print('Ejecutando objdump')
                output = subprocess.check_output(['ssh', 'analista@' + ip, 'objdump', '-d', rutaUser + '/' + malware], shell=True)
                buffer = io.StringIO(output.decode())
                with open(rutaHost+'/Mlwr_Lab_Work_Dir/Experimentos/'+str(eid)+'/'+str(sid)+'/objdump-'+date+'.txt', 'w') as archivo:
                    archivo.write(buffer.getvalue())
                archivo.close()
                
            if strace == 'true':
                print('Ejecutando strace')
                output = subprocess.check_output(['ssh', 'analista@' + ip, 'strace', rutaUser + '/' + malware], shell=True)
                buffer = io.StringIO(output.decode())
                with open(rutaHost+'/Mlwr_Lab_Work_Dir/Experimentos/'+str(eid)+'/'+str(sid)+'/strace-'+date+'.txt', 'w') as archivo:
                    archivo.write(buffer.getvalue())
                archivo.close()

    elif os.path.isfile(mwRuta):
        print(get_filename_from_path(mwRuta))
        mw_name = get_filename_from_path(mwRuta)
        
        print(f'{mw_name} es un archivo')

        # Envía el malware al laboratorio
        subprocess.run(["SCP", mwRuta, "analista@" + ip + ":" + rutaUser])

        print("Procesando archivo: " + mw_name)
        
        muestraDir = os.path.join(rutaHost+ '/Mlwr_Lab_Work_Dir/Experimentos/'+ str(eid), '/')
        sid = len(os.listdir(muestraDir)) + 1
        new_muestra_dir = os.path.join(muestraDir, str(sid))
        os.mkdir(new_muestra_dir)

        # Aplicamos las pruebas seleccionadas en el JSON
        if fileTest == 'true':
            print("Ejecutando file")
            output = subprocess.check_output(["ssh", "analista@" + ip, "file", rutaUser + "/" + mw_name], shell=True)
            buffer = io.StringIO(output.decode())
            with open(rutaHost+'/Mlwr_Lab_Work_Dir/Experimentos/'+str(eid)+'/'+str(sid)+'/file-'+date+'.txt', 'w') as archivo:
                archivo.write(buffer.getvalue())
            archivo.close()

        if exiftool == 'true':
            print("Ejecutando exiftool")
            output = subprocess.check_output(["ssh", "analista@" + ip, "exiftool", rutaUser + "/" + mw_name], shell=True)
            buffer = io.StringIO(output.decode())
            with open(rutaHost+'/Mlwr_Lab_Work_Dir/Experimentos/'+str(eid)+'/'+str(sid)+'/exiftool-'+date+'.txt', 'w') as archivo:
                archivo.write(buffer.getvalue())
            archivo.close()

        if md5 == 'true':
            print('Ejecutando MD5')
            output = subprocess.check_output(['ssh', 'analista@' + ip, 'md5sum', rutaUser + "/" + mw_name], shell=True)
            buffer = io.StringIO(output.decode())
            with open(rutaHost+'/Mlwr_Lab_Work_Dir/Experimentos/'+str(eid)+'/'+str(sid)+'/md5-'+date+'.txt', 'w') as archivo:
                archivo.write(buffer.getvalue())
            archivo.close()

        if sha1 == 'true':
            print('Ejecutando SHA1')
            output = subprocess.check_output(['ssh', 'analista@' + ip, 'sha1sum', rutaUser + "/" + mw_name], shell=True)
            buffer = io.StringIO(output.decode())
            with open(rutaHost+'/Mlwr_Lab_Work_Dir/Experimentos/'+str(eid)+'/'+str(sid)+'/sha1-'+date+'.txt', 'w') as archivo:
                archivo.write(buffer.getvalue())
            archivo.close()
            
        if sha256 == 'true':
            print('Ejecutando SHA256')
            output = subprocess.check_output(['ssh', 'analista@' + ip, 'sha256sum', rutaUser + '/' + mw_name], shell=True)
            buffer = io.StringIO(output.decode())
            with open(rutaHost+'/Mlwr_Lab_Work_Dir/Experimentos/'+str(eid)+'/'+str(sid)+'/sha256-'+date+'.txt', 'w') as archivo:
                archivo.write(buffer.getvalue())
            archivo.close()
            
        if objdump == 'true':
            print('Ejecutando objdump')
            output = subprocess.check_output(['ssh', 'analista@' + ip, 'objdump', '-d', rutaUser + '/' + mw_name], shell=True)
            buffer = io.StringIO(output.decode())
            with open(rutaHost+'/Mlwr_Lab_Work_Dir/Experimentos/'+str(eid)+'/'+str(sid)+'/objdump-'+date+'.txt', 'w') as archivo:
                archivo.write(buffer.getvalue())
            archivo.close()

        if strace == 'true':
            print('Ejecutando strace')
            output = subprocess.check_output(['ssh', 'analista@' + ip, 'strace', rutaUser + '/' + mw_name], shell=True)
            buffer = io.StringIO(output.decode())
            with open(rutaHost+'/Mlwr_Lab_Work_Dir/Experimentos/'+str(eid)+'/'+str(sid)+'/strace-'+date+'.txt', 'w') as archivo:
                archivo.write(buffer.getvalue())
            archivo.close()

    elif (mwRuta == NULL and mwUrl != NULL):
        print(f'{mwUrl} Es un url a descargar desde MAREA')

    else:
        print('No hay muestra a usar')

    # Copiar el archivo de configuración JSON en el experimento creado
    src = os.path.join(rutaHost+ '/Mlwr_Lab_Work_Dir/Configuraciones/scripts/'+ ruta_archivo+ '/configuracion.json')
    dst = os.path.join(rutaHost+ '/Mlwr_Lab_Work_Dir/Experimentos/'+ str(eid)+ '/configuracion.json')

    shutil.copyfile(src, dst)

    # Copiar el archivo de dataset JSON en el experimento creado
    src = os.path.join(rutaHost+ '/Mlwr_Lab_Work_Dir/Configuraciones/scripts/'+ ruta_archivo+ '/dataset.json')
    dst = os.path.join(rutaHost+ '/Mlwr_Lab_Work_Dir/Experimentos/'+ str(eid)+ '/dataset.json')

    shutil.copyfile(src, dst)
    
    #subprocess.run(["VBoxManage", "controlvm", nameVM, "poweroff"])
    #subprocess.run(["VBoxManage", "snapshot", nameVM, "restore", snapshot])

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('Debe especificar el tipo de pruebas que deseas correr.')
    else:
        ruta_archivo = sys.argv[1]
        leer_archivo_json(ruta_archivo)
    