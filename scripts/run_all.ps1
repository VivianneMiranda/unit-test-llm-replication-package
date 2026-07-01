#Requires -Version 5.1
<#
.SYNOPSIS
    Master script: setup projects, parse existing results, aggregate tables.
#>
param(
    [switch]$Setup,
    [switch]$ParseOnly,
    [switch]$Figures
)

$ErrorActionPreference = "Stop"
$Root = Resolve-Path "$PSScriptRoot\.."

Write-Host @"
[run_all] Package scope: BCEL + CLI only (see docs/package-scope.md)
          Optional: .\scripts\archive_metrics_from_target.ps1
"@

if ($Setup) {
    Write-Warning "00_setup clones all 5 paper projects; not required for this artifact."
    & "$PSScriptRoot\00_setup.ps1"
}

if (-not $ParseOnly) {
    Write-Host @"

[run_all] To archive existing target/ reports:
          .\scripts\archive_metrics_from_target.ps1

"@
}

Write-Host "[run_all] Parsing all available raw results..."
python "$PSScriptRoot\04_parse_results.py" --all

$aggArgs = @("$PSScriptRoot\05_aggregate_tables.py")
if ($Figures) { $aggArgs += "--figures" }
python @aggArgs

Write-Host "[run_all] Done. See results/processed/ and results/STATUS.md"
