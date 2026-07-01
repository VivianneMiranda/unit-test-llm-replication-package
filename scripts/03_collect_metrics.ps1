#Requires -Version 5.1
param(
    [Parameter(Mandatory = $true)]
    [ValidateSet("bcel", "cli", "collections", "compress", "lang")]
    [string]$Project,

    [Parameter(Mandatory = $true)]
    [ValidateSet("developer", "opus-4.5", "sonnet-4.5", "gpt-5.1-codex-max")]
    [string]$Origin
)

$ErrorActionPreference = "Stop"
$Root = Resolve-Path "$PSScriptRoot\.."
$config = Get-Content "$Root\config\projects.json" -Raw | ConvertFrom-Json
$proj = $config.projects | Where-Object { $_.id -eq $Project }

$projectDir = & python "$PSScriptRoot\resolve_project_path.py" $Project $Origin
if (-not $projectDir -or -not (Test-Path $projectDir)) {
    throw "Project not found at '$projectDir'. Run scripts/00_setup.ps1 or add paths in config/artifact-locations.json."
}
Write-Host "[path] Using $projectDir"

$rawOut = Join-Path $Root "results\raw\$Project\$Origin"
New-Item -ItemType Directory -Force -Path $rawOut | Out-Null

Push-Location $projectDir
try {
    Write-Host "[maven] JaCoCo: $($proj.name) / $Origin"
    mvn clean test jacoco:report
    if ($LASTEXITCODE -ne 0) { throw "JaCoCo build failed with exit code $LASTEXITCODE" }

    $jacocoSrc = Join-Path $projectDir "target\site\jacoco"
    if (Test-Path $jacocoSrc) {
        $jacocoDest = Join-Path $rawOut "jacoco"
        if (Test-Path $jacocoDest) { Remove-Item -Recurse -Force $jacocoDest }
        Copy-Item -Recurse $jacocoSrc $jacocoDest
    }

    Write-Host "[maven] PIT: $($proj.name) / $Origin (this may take a long time)"
    mvn test org.pitest:pitest-maven:mutationCoverage
    if ($LASTEXITCODE -ne 0) { throw "PIT failed with exit code $LASTEXITCODE" }

    $pitReports = Get-ChildItem -Path (Join-Path $projectDir "target\pit-reports") -ErrorAction SilentlyContinue
    if ($pitReports) {
        $latest = $pitReports | Sort-Object LastWriteTime -Descending | Select-Object -First 1
        $pitDest = Join-Path $rawOut "pit"
        if (Test-Path $pitDest) { Remove-Item -Recurse -Force $pitDest }
        Copy-Item -Recurse $latest.FullName $pitDest
    }

    Write-Host "[metrics] Reports copied to $rawOut"
    & python "$PSScriptRoot\04_parse_results.py" --project $Project --origin $Origin
}
finally {
    Pop-Location
}
