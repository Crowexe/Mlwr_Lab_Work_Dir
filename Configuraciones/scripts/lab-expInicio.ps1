param($jsonFolder)

$params = Get-Content C:\Users\Crow9\Desktop\Mlwr_Lab_Work_Dir\Configuraciones\scripts\$jsonFolder\dataset.json | ConvertFrom-Json

$rutaHost = $params.rutaHost

$eid = (Get-ChildItem $rutaHost\Mlwr_Lab_Work_Dir\Experimentos).Count + 1

mkdir $rutaHost\Mlwr_Lab_Work_Dir\Experimentos\$eid

Copy-Item "C:\Users\Crow9\Desktop\Mlwr_Lab_Work_Dir\Configuraciones\scripts\$jsonFolder\configuracion.json" -Destination "$rutaHost\Mlwr_Lab_Work_Dir\Experimentos\$eid"

Copy-Item "C:\Users\Crow9\Desktop\Mlwr_Lab_Work_Dir\Configuraciones\scripts\$jsonFolder\dataset.json" -Destination "$rutaHost\Mlwr_Lab_Work_Dir\Experimentos\$eid"