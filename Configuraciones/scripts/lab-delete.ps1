param($tipoVM)
$params = Get-Content C:\Users\Crow9\Desktop\Mlwr_Lab_Work_Dir\Configuraciones\maq_virt\$tipoVM\configuracion.json | ConvertFrom-Json 
$nameVM = $params.nombre

VBoxManage unregistervm $nameVM --delete