function VerificarDependencias { # Verificar integridad de las dependencias
    $requirements = Get-Content -Path "requirements.txt"
    $installed = & .\venv\Scripts\python.exe -m pip freeze

    foreach ($requirement in $requirements) {
        if ($installed -notcontains $requirement) {
            Write-Output "Dependencia faltante o incorrecta: $requirement"
            return $false
        }
    }
    returne $true
}

if (Test-Path -Path .\venv) {
    Write-Output "El entorno virtual ya existe. Verificando dependencias..."
    .\venv\Scripts\Activate.ps1

    if(-not (VerificarDependencias)) {
        Write-Output "Las dependencias no están completas o son incorrectas. Reinstalando..."
        pip install -r requirements.txt
        Write-Output "Las dependencias han sido reinstaladas."
    } else {
        Write-Output "Dependencias validadas."
    }
    Write-Output "Entorno inicializado."
} else {
    Write-Output "El entorno virtual no existe. Creando nuevo entorno..."
    python -m venv venv
    .\venv\Scripts\Activate.ps1
    pip install --upgrade pip
    pip install -r requirements.txt
    Write-Output "El enorno vistual ha sido inicializado y las librerias han sido instaladas correctamente.\n"
}

Write-Output "Ejecute el script 'python ./src/app.py' para iniciar el servidor"
Write-Output "NOTA: Si con el comando 'python' no lo inicializa, ejecutelo con 'python3' o con 'py'"