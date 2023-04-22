param($jsonFolder)

$params = Get-Content C:\Users\Crow9\Desktop\Mlwr_Lab_Work_Dir\Configuraciones\maq_virt\$jsonFolder\configuracion.json | ConvertFrom-Json

$baseVM = $params.baseVM
$tipoVM = $params.tipo
$ip = $params.ipCmd
$nameVM = $params.nombre
$rutaHost = $params.rutaHost
$snapshot = $params.snapshot

if ($tipoVM -eq 'estatica') {
    VBoxManage clonevm $baseVM --name="$nameVM" --basefolder="$rutaHost\Mlwr_Lab_Work_Dir" --register --snapshot="$snapshot"
    VBoxManage startvm LabStatic --type headless   
    VBoxManage snapshot LabStatic take StaticShot

} elseif ($tipoVM -eq 'dinamica') {
    VBoxManage clonevm $originVM --name="$nameVM" --basefolder="$LocDisk\$locFolder\$locUser\Desktop\Mlwr_Lab_Work_Dir" --register --snapshot="$snapshot"
    VBoxManage startvm LabDinamic --type headless
    VBoxManage snapshot LabDinamic take DinamicShot
}