#Requires -Version 5.1
<#
.SYNOPSIS
    Organize published metrics and regenerate aggregated tables.
#>
param(
    [switch]$Setup,
    [switch]$Figures
)

$ErrorActionPreference = "Stop"
$Root = Resolve-Path "$PSScriptRoot\.."

Write-Host @"
[run_all] Light replication package — published metrics + reproduction scripts
          See docs/package-scope.md
"@

if ($Setup) {
    & "$PSScriptRoot\00_setup.ps1"
}

Write-Host "[run_all] Organizing published per-class metrics..."
python "$PSScriptRoot\organize_published_metrics.py" --keep-source

$aggArgs = @("$PSScriptRoot\05_aggregate_tables.py")
if ($Figures) { $aggArgs += "--figures" }
python @aggArgs

Write-Host "[run_all] Done. See results/per-class/, results/processed/, and results/STATUS.md"
