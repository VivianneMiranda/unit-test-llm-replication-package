#Requires -Version 5.1
<#
.SYNOPSIS
    Remove all existing tests to prepare for LLM generation.
#>
param(
    [Parameter(Mandatory = $true)]
    [ValidateSet("bcel", "cli", "collections", "compress", "lang")]
    [string]$Project,
    [switch]$Force
)

$ErrorActionPreference = "Stop"
$Root = Resolve-Path "$PSScriptRoot\.."
$config = Get-Content "$Root\config\projects.json" -Raw | ConvertFrom-Json
$proj = $config.projects | Where-Object { $_.id -eq $Project }
$projectDir = Join-Path $Root $proj.directory
$testDir = Join-Path $projectDir "src\test\java"

if (-not (Test-Path $projectDir)) {
    throw "Project not found. Run scripts/00_setup.ps1 first."
}

if (-not $Force) {
    $answer = Read-Host "This will DELETE all tests under $testDir. Continue? [y/N]"
    if ($answer -notmatch '^[yY]') { exit 0 }
}

if (Test-Path $testDir) {
    Remove-Item -Recurse -Force $testDir
}
New-Item -ItemType Directory -Force -Path $testDir | Out-Null
Write-Host "[prepare] Removed all tests from $($proj.name). Ready for LLM generation."
