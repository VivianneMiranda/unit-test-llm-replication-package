#Requires -Version 5.1
<#
.SYNOPSIS
    Copy JaCoCo and PIT reports from commons-bcel/cli target/ into results/raw/.
.DESCRIPTION
    Archives locally executed metrics without re-running Maven.
#>
$ErrorActionPreference = "Stop"
$Root = Resolve-Path "$PSScriptRoot\.."
$locations = Get-Content "$Root\config\artifact-locations.json" -Raw | ConvertFrom-Json
$scope = Get-Content "$Root\config\package-scope.json" -Raw | ConvertFrom-Json

foreach ($projectId in $scope.included_project_ids) {
    $origins = $locations.$projectId.PSObject.Properties
    foreach ($prop in $origins) {
        if ($prop.Name -eq "description" -or $prop.Name -eq "naming_notes") { continue }
        $origin = $prop.Name
        $relPath = $prop.Value
        $projectDir = Join-Path $Root ($relPath -replace '/', '\')
        $rawOut = Join-Path $Root "results\raw\$projectId\$origin"

        if (-not (Test-Path $projectDir)) {
            Write-Warning "[skip] Missing $projectDir"
            continue
        }

        New-Item -ItemType Directory -Force -Path $rawOut | Out-Null
        $copied = $false

        $jacocoSrc = Join-Path $projectDir "target\site\jacoco"
        if (Test-Path $jacocoSrc) {
            $jacocoDest = Join-Path $rawOut "jacoco"
            if (Test-Path $jacocoDest) { Remove-Item -Recurse -Force $jacocoDest }
            Copy-Item -Recurse $jacocoSrc $jacocoDest
            Write-Host "[archive] $projectId/$origin jacoco"
            $copied = $true
        }

        $pitRoot = Join-Path $projectDir "target\pit-reports"
        if (Test-Path $pitRoot) {
            $pitDest = Join-Path $rawOut "pit"
            if (Test-Path $pitDest) { Remove-Item -Recurse -Force $pitDest }
            Copy-Item -Recurse $pitRoot $pitDest
            Write-Host "[archive] $projectId/$origin pit-reports"
            $copied = $true
        }

        if (-not $copied) {
            Write-Warning "[skip] No target reports for $projectId/$origin"
        }
    }
}

Write-Host "Done. Run: python scripts\04_parse_results.py --all"
