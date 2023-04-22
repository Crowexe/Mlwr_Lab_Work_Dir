param($jsonFolder)

$config = Get-Content C:\Users\Crow9\Desktop\Mlwr_Lab_Work_Dir\Configuraciones\scripts\$jsonFolder\configuracion.json | ConvertFrom-Json

$dataset = Get-Content C:\Users\Crow9\Desktop\Mlwr_Lab_Work_Dir\Configuraciones\scripts\$jsonFolder\dataset.json | ConvertFrom-Json

$nameVM = $config.nameVM
$snapshot = $config.snapshot
$rutaUser = $config.rutaUser
$rutaHost = $config.rutaHost
$ip = $config.ipCmd
$mwUrl = $dataset.malware.url
$mwRuta = $dataset.malware.ruta
$file = $dataset.pruebas.estaticas.file
$exiftool = $dataset.pruebas.estaticas.exiftool
$MD5 = $dataset.pruebas.estaticas.MD5
$SHA1 = $dataset.pruebas.estaticas.SHA1
$SHA256 = $dataset.pruebas.estaticas.SHA256
$objdump = $dataset.pruebas.dinamicas.objdump
$strace = $dataset.pruebas.dinamicas.strace

function Get-FilenameFromPath {
    param(
        [Parameter(Mandatory=$true)]
        [string]$mwRuta
    )

    $mwName = Split-Path $mwRuta -Leaf
    return $mwName
}

#SCP $mwRuta "analista@${ip}:$rutaUser"

VBoxManage startvm $nameVM --type headless

$date = Get-Date -Format yyyyMMdd-HHmmss

$eid = (Get-ChildItem $rutaHost\Mlwr_Lab_Work_Dir\Experimentos).Count + 1

mkdir "$rutaHost\Mlwr_Lab_Work_Dir\Experimentos\$eid"

Copy-Item "$rutaHost\Mlwr_Lab_Work_Dir\Configuraciones\scripts\$jsonFolder\configuracion.json" -Destination "$rutaHost\Mlwr_Lab_Work_Dir\Experimentos\$eid"

Copy-Item "C:\Users\Crow9\Desktop\Mlwr_Lab_Work_Dir\Configuraciones\scripts\$jsonFolder\dataset.json" -Destination "$rutaHost\Mlwr_Lab_Work_Dir\Experimentos\$eid"

if ((Get-Item $mwRuta).PSIsContainer) {
    $malwares = Get-ChildItem $mwRuta

    foreach ($malware in $malwares) {

        Write-Host "Procesando archivo: $($malware.Name)"
        SCP "$mwRuta\$($malware.Name)" "analista@${ip}:$rutaUser"
        
        $sid = (Get-ChildItem $rutaHost\Mlwr_Lab_Work_Dir\Experimentos\$eid -Directory).Count + 1
        mkdir "$rutaHost\Mlwr_Lab_Work_Dir\Experimentos\$eid\$sid"

        $mwName = Get-FilenameFromPath $mwRuta

        #Copy-Item $malware.FullName "$rutaHost\Mlwr_Lab_Work_Dir\Experimentos\$eid\$sid"

        if($file -eq 'true'){
            $ruta = "$rutaHost\Mlwr_Lab_Work_Dir\Experimentos\$eid\$sid\file-$date.txt"
            ssh analista@$ip "file $rutaUser/$($malware.Name)" 
            ssh analista@$ip "file $rutaUser/$($malware.Name)" | Out-File -FilePath $ruta  
        }
        if($exiftool -eq 'true'){
            $ruta = "$rutaHost\Mlwr_Lab_Work_Dir\Experimentos\$eid\$sid\exiftool-$date.txt"
            ssh analista@$ip "exiftool $rutaUser/$($malware.Name)" 
            ssh analista@$ip "exiftool $rutaUser/$($malware.Name)" | Out-File -FilePath $ruta  
        }
        if($MD5 -eq 'true'){
            $ruta = "$rutaHost\Mlwr_Lab_Work_Dir\Experimentos\$eid\$sid\MD5-$date.txt"
            ssh analista@$ip "md5sum $rutaUser/$($malware.Name)" 
            ssh analista@$ip "md5sum $rutaUser/$($malware.Name)" | Out-File -FilePath $ruta  
        }
        if($SHA1 -eq 'true'){
            $ruta = "$rutaHost\Mlwr_Lab_Work_Dir\Experimentos\$eid\$sid\SHA1-$date.txt"
            ssh analista@$ip "sha1sum $rutaUser/$($malware.Name)" 
            ssh analista@$ip "sha1sum $rutaUser/$($malware.Name)" | Out-File -FilePath $ruta  
        }
        if($SHA256 -eq 'true'){
            $ruta = "$rutaHost\Mlwr_Lab_Work_Dir\Experimentos\$eid\$sid\SHA256-$date.txt"
            ssh analista@$ip "sha256sum $rutaUser/$($malware.Name)" 
            ssh analista@$ip "sha256sum $rutaUser/$($malware.Name)" | Out-File -FilePath $ruta  
        }
        if($objdump -eq 'true'){
            $ruta = "$rutaHost\Mlwr_Lab_Work_Dir\Experimentos\$eid\$sid\objdump-$date.txt"
            ssh analista@$ip "objdump -d $rutaUser/$($malware.Name)" 
            ssh analista@$ip "objdump -d $rutaUser/$($malware.Name)" | Out-File -FilePath $ruta  
        }
        if($strace -eq 'true'){
            $ruta = "$rutaHost\Mlwr_Lab_Work_Dir\Experimentos\$eid\$sid\strace-$date.txt"
            ssh analista@$ip "strace $rutaUser/$($malware.Name)" 
            ssh analista@$ip "strace $rutaUser/$($malware.Name)" | Out-File -FilePath $ruta  
        }
    }
}
elseif ($mwUrl -ne "" -and $mwRuta -eq "") {
    Write-Host "Es algo descargable"
    ssh analista@$ip "curl -H 'Authorization:9b531ce8e5c04153a4054b2ff02c7e7c9eeaf0e367b34c15bc1e5f8972c1e24f' -o $rutaUser $mwUrl"
    ssh analista@ip "7z $mwName.zip -p infected -o $rutaUser"

    $sid = (Get-ChildItem $rutaHost\Mlwr_Lab_Work_Dir\Experimentos\$eid -Directory).Count + 1
    mkdir "$rutaHost\Mlwr_Lab_Work_Dir\Experimentos\$eid\$sid"

    $mwName = Get-FilenameFromPath $mwRuta

    if($file -eq 'true'){
        
        $ruta = "$rutaHost\Mlwr_Lab_Work_Dir\Experimentos\$eid\$sid\file-$date.txt"
        ssh analista@$ip "file $mwName" 
        ssh analista@$ip "file $mwName" | Out-File -FilePath $ruta  
    } 
    if($exiftool -eq 'true'){
        $ruta = "$rutaHost\Mlwr_Lab_Work_Dir\Experimentos\$eid\$sid\exiftool-$date.txt"
        ssh analista@$ip "exiftool $mwName" 
        ssh analista@$ip "exiftool $mwName" | Out-File -FilePath $ruta  
    }
    if($MD5 -eq 'true'){
        $ruta = "$rutaHost\Mlwr_Lab_Work_Dir\Experimentos\$eid\$sid\MD5-$date.txt"
        ssh analista@$ip "md5sum $mwName" 
        ssh analista@$ip "md5sum $mwName" | Out-File -FilePath $ruta  
    }
    if($SHA1 -eq 'true'){
        $ruta = "$rutaHost\Mlwr_Lab_Work_Dir\Experimentos\$eid\$sid\SHA1-$date.txt"
        ssh analista@$ip "sha1sum $mwName" 
        ssh analista@$ip "sha1sum $mwName" | Out-File -FilePath $ruta  
    }
    if($SHA256 -eq 'true'){
        $ruta = "$rutaHost\Mlwr_Lab_Work_Dir\Experimentos\$eid\$sid\SHA256-$date.txt"
        ssh analista@$ip "sha256sum $mwName" 
        ssh analista@$ip "sha256sum $mwName" | Out-File -FilePath $ruta  
    }
    if($objdump -eq 'true'){
        $ruta = "$rutaHost\Mlwr_Lab_Work_Dir\Experimentos\$eid\$sid\objdump-$date.txt"
        ssh analista@$ip "objdump -d $mwName" 
        ssh analista@$ip "objdump -d $mwName" | Out-File -FilePath $ruta  
    }
    if($strace -eq 'true'){
        $ruta = "$rutaHost\Mlwr_Lab_Work_Dir\Experimentos\$eid\$sid\strace-$date.txt"
        ssh analista@$ip "strace $mwName" 
        ssh analista@$ip "strace $mwName" | Out-File -FilePath $ruta  
    }

}
else {

    SCP $mwRuta "analista@${ip}:$rutaUser"

    $sid = (Get-ChildItem $rutaHost\Mlwr_Lab_Work_Dir\Experimentos\$eid -Directory).Count + 1
    mkdir "$rutaHost\Mlwr_Lab_Work_Dir\Experimentos\$eid\$sid"

    $mwName = Get-FilenameFromPath $mwRuta 

    if($file -eq 'true'){
        
        $ruta = "$rutaHost\Mlwr_Lab_Work_Dir\Experimentos\$eid\$sid\file-$date.txt"
        ssh analista@$ip "file $mwName" 
        ssh analista@$ip "file $mwName" | Out-File -FilePath $ruta  
    } 
    if($exiftool -eq 'true'){
        $ruta = "$rutaHost\Mlwr_Lab_Work_Dir\Experimentos\$eid\$sid\exiftool-$date.txt"
        ssh analista@$ip "exiftool $mwName" 
        ssh analista@$ip "exiftool $mwName" | Out-File -FilePath $ruta  
    }
    if($MD5 -eq 'true'){
        $ruta = "$rutaHost\Mlwr_Lab_Work_Dir\Experimentos\$eid\$sid\MD5-$date.txt"
        ssh analista@$ip "md5sum $mwName" 
        ssh analista@$ip "md5sum $mwName" | Out-File -FilePath $ruta  
    }
    if($SHA1 -eq 'true'){
        $ruta = "$rutaHost\Mlwr_Lab_Work_Dir\Experimentos\$eid\$sid\SHA1-$date.txt"
        ssh analista@$ip "sha1sum $mwName" 
        ssh analista@$ip "sha1sum $mwName" | Out-File -FilePath $ruta  
    }
    if($SHA256 -eq 'true'){
        $ruta = "$rutaHost\Mlwr_Lab_Work_Dir\Experimentos\$eid\$sid\SHA256-$date.txt"
        ssh analista@$ip "sha256sum $mwName" 
        ssh analista@$ip "sha256sum $mwName" | Out-File -FilePath $ruta  
    }
    if($objdump -eq 'true'){
        $ruta = "$rutaHost\Mlwr_Lab_Work_Dir\Experimentos\$eid\$sid\objdump-$date.txt"
        ssh analista@$ip "objdump -d $mwName" 
        ssh analista@$ip "objdump -d $mwName" | Out-File -FilePath $ruta  
    }
    if($strace -eq 'true'){
        $ruta = "$rutaHost\Mlwr_Lab_Work_Dir\Experimentos\$eid\$sid\strace-$date.txt"
        ssh analista@$ip "strace $mwName" 
        ssh analista@$ip "strace $mwName" | Out-File -FilePath $ruta  
    }
}

#VBoxManage startvm $nameVM --type headless
#VBoxManage snapshot $nameVM restore $snapshot 