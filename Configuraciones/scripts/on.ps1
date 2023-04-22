param($json)

$params = Get-Content C:\Users\Crow9\Desktop\Mlwr_Lab_Work_Dir\Configuraciones\maq_virt\$json\configuracion.json | ConvertFrom-Json 

$nameVM = $params.nombre

VBoxManage startvm $nameVM --type headless