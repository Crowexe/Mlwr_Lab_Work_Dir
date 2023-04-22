param($tipoVM)

$params = Get-Content C:\Users\Crow9\Desktop\Mlwr_Lab_Work_Dir\Configuraciones\maq_virt\$tipoVM\configuracion.json | ConvertFrom-Json

$baseVM = $params.baseVM
$ip = $params.ipCmd
$nameVM = $params.nombre
$rutaHost = $params.rutaHost
$snapshot = $params.snapshot

VBoxManage clonevm $baseVM --name="$nameVM" --basefolder="$rutaHost" --register --snapshot="$snapshot"