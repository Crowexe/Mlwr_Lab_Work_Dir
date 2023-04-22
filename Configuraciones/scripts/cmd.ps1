param($jsonFolder,$comando)

$config = Get-Content C:\Users\Crow9\Desktop\Mlwr_Lab_Work_Dir\Configuraciones\scripts\$jsonFolder\configuracion.json | ConvertFrom-Json 

$ip = $config.ipCmd

ssh analista@$ip $comando