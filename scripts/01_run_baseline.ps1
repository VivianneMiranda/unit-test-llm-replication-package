#Requires -Version 5.1
param(
    [Parameter(Mandatory = $true)]
    [ValidateSet("bcel", "cli", "collections", "compress", "lang")]
    [string]$Project
)

$ErrorActionPreference = "Stop"
$Root = Resolve-Path "$PSScriptRoot\.."
$config = Get-Content "$Root\config\projects.json" -Raw | ConvertFrom-Json
$proj = $config.projects | Where-Object { $_.id -eq $Project }
if (-not $proj) { throw "Unknown project: $Project" }

$projectDir = Join-Path $Root $proj.directory
if (-not (Test-Path $projectDir)) {
    throw "Project not found. Run scripts/00_setup.ps1 first."
}

$logDir = Join-Path $Root "logs\maven"
New-Item -ItemType Directory -Force -Path $logDir | Out-Null
$logFile = Join-Path $logDir "baseline-$Project-$(Get-Date -Format 'yyyyMMdd-HHmmss').log"

Write-Host "[baseline] Running metrics for $($proj.name) (developer suite)"
Push-Location $projectDir
try {
    & "$PSScriptRoot\03_collect_metrics.ps1" -Project $Project -Origin developer 2>&1 | Tee-Object -FilePath $logFile
}
finally {
    Pop-Location
}

Write-Host "[baseline] Done. Log: $logFile"
