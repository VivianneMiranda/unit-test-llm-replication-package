#Requires -Version 5.1
<#
.SYNOPSIS
    Clone Apache Commons projects at exact study versions.
.DESCRIPTION
    Optional: clones all five paper projects. This artifact only requires
    commons-bcel/ and commons-cli/ at the repo root. See docs/package-scope.md.
#>
param(
    [string]$ConfigPath = "$PSScriptRoot\..\config\projects.json"
)

$ErrorActionPreference = "Stop"
$Root = Resolve-Path "$PSScriptRoot\.."
$config = Get-Content $ConfigPath -Raw | ConvertFrom-Json

foreach ($project in $config.projects) {
    $dest = Join-Path $Root $project.directory
    if (Test-Path (Join-Path $dest ".git")) {
        Write-Host "[skip] $($project.name) already cloned at $dest"
        continue
    }
    Write-Host "[clone] $($project.name) tag $($project.git_tag) -> $dest"
    New-Item -ItemType Directory -Force -Path $dest | Out-Null
    git clone --depth 1 --branch $project.git_tag $project.git_url $dest
    if ($LASTEXITCODE -ne 0) {
        Write-Warning "Shallow clone failed for $($project.id); trying full clone + checkout"
        if (Test-Path $dest) { Remove-Item -Recurse -Force $dest }
        git clone $project.git_url $dest
        Push-Location $dest
        git checkout $project.git_tag
        Pop-Location
    }
}

Write-Host "Setup complete. Projects are under projects/"
