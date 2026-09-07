[CmdletBinding()]
param(
    [string]$EnvFile,
    [switch]$Apply,
    [switch]$Yes,
    [switch]$Help
)
$ErrorActionPreference = "Stop"
$WorkshopSrc = (Resolve-Path (Join-Path $PSScriptRoot "..")).Path
$WorkshopRoot = (Resolve-Path (Join-Path $WorkshopSrc "..")).Path
if ($Help) {
    Write-Host "Usage: ./provision.ps1 [-EnvFile PATH] [-Apply] [-Yes]"
    Write-Host "Default runs an Azure what-if. -Apply can create billable resources."
    exit 0
}
if (-not $EnvFile) { $EnvFile = Join-Path $WorkshopRoot ".env" }
& (Join-Path $PSScriptRoot "preflight.ps1") -EnvFile $EnvFile -Online
if ($LASTEXITCODE -ne 0) { throw "Preflight failed." }
Push-Location $WorkshopSrc
try {
    if (-not $Apply) {
        & azd provision --preview --no-prompt
        if ($LASTEXITCODE -ne 0) { throw "Preview failed." }
        Write-Host "[OK] Preview complete; no resources changed."
        exit 0
    }
    if (-not $Yes -and (Read-Host "Type PROVISION to create chargeable resources") -ne "PROVISION") {
        throw "Cancelled."
    }
    & azd provision --no-prompt
    if ($LASTEXITCODE -ne 0) { throw "Provisioning failed." }
} finally { Pop-Location }
Write-Host "[OK] Provisioning completed."
