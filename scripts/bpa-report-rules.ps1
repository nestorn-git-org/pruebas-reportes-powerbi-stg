param (
    [string]$src
)
# comment: test
$cliPath = "$PSScriptRoot\..\_tools\PBIInspector\win-x64\CLI\PBIRInspectorCLI.exe"
$rulesPath = "$PSScriptRoot\..\test\bpa-report-rules.json"

if (!(Test-Path $cliPath)) {
    throw "PBIRInspectorCLI.exe no encontrado en '$cliPath'. Asegúrate de que esté presente en el repositorio."
}

if (!(Test-Path $rulesPath)) {
    throw "Archivo de reglas no encontrado en '$rulesPath'."
}

$itemsFolders = Get-ChildItem -Path $src -Recurse -Include "*.pb*"

foreach ($itemFolder in $itemsFolders) {
    $itemPath = Join-Path $itemFolder.Directory.FullName "definition"

    if (!(Test-Path $itemPath)) {
        throw "No se encontró la definición PBIR en '$itemPath'. Convierte el archivo legacy con Power BI Desktop."
    }

    Write-Host "Ejecutando reglas BPA para: '$itemPath'"

    $process = Start-Process -FilePath $cliPath `
        -ArgumentList "-pbipreport `"$itemPath`" -rules `"$rulesPath`" -formats `"GitHub`"" `
        -NoNewWindow -Wait -PassThru

    if ($process.ExitCode -ne 0) {
        throw "Error al ejecutar BPA para: '$itemPath'"
    }
}

Write-Host "Ejecución completada!"