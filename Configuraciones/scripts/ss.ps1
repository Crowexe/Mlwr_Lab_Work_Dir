param($jsonFolder)

$params = Get-Content C:\Users\Crow9\Desktop\Mlwr_Lab_Work_Dir\Configuraciones\maq_virt\$jsonFolder\configuracion.json | ConvertFrom-Json

$nameVM = $params.nombre
$SS = $params.snapshotNew

VBoxManage snapshot $nameVM take $SS