param (
    [string]$src
)

$cliPath = "$PSScriptRoot\..\_tools\PBIInspector\win-x64\CLI\PBIRInspectorCLI.exe"
$rulesPath = "$PSScriptRoot\..\test\bpa-semantic-rules.json"

if (!(Test-Path $cliPath)) {
    throw "PBIRInspectorCLI.exe no encontrado en '$cliPath'. Asegúrate de que esté presente en el repositorio."
}

if (!(Test-Path $rulesPath)) {
    throw "Archivo de reglas no encontrado en '$rulesPath'."
}

$itemsFolders = Get-ChildItem -Path $src -Recurse -Include "*.pbim"

foreach ($itemFolder in $itemsFolders) {
    $itemPath = Join-Path $itemFolder.Directory.FullName "model.bim"

    if (!(Test-Path $itemPath)) {
        throw "No se encontró el archivo 'model.bim' en '$itemPath'."
    }

    Write-Host "Ejecutando reglas BPA para modelo semántico: '$itemPath'"

    $process = Start-Process -FilePath $cliPath `
        -ArgumentList "-pbipmodel `"$itemPath`" -rules `"$rulesPath`" -formats `"GitHub`"" `
        -NoNewWindow -Wait -PassThru

    if ($process.ExitCode -ne 0) {
        throw "Error al ejecutar BPA para modelo semántico: '$itemPath'"
    }
}

Write-Host "Ejecución completada!"