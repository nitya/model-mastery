[CmdletBinding()]
param([switch]$Apply, [switch]$Yes, [switch]$Help)
$ErrorActionPreference = "Stop"
$WorkshopSrc = (Resolve-Path (Join-Path $PSScriptRoot "..")).Path
if ($Help) {
    Write-Host "Usage: ./cleanup.ps1 [-Apply] [-Yes]"
    Write-Host "Default lists the target; -Apply runs azd down --purge --force."
    exit 0
}
Push-Location $WorkshopSrc
try {
    $group = & azd env get-value AZURE_RESOURCE_GROUP 2>$null
    Write-Host "Target resource group: $group"
    if ($group) {
        & az resource list --resource-group $group `
            --query "[].{name:name,type:type,location:location}" --output table
    }
    if (-not $Apply) { Write-Host "[OK] Preview only; nothing deleted."; exit 0 }
    if (-not $group) { throw "AZURE_RESOURCE_GROUP is not set." }
    if (-not $Yes -and (Read-Host "Type DELETE to permanently remove the group") -ne "DELETE") {
        throw "Cancelled."
    }
    & azd down --purge --force
    if ($LASTEXITCODE -ne 0) { throw "Cleanup failed." }
} finally { Pop-Location }
Write-Host "[OK] azd-managed workshop resources deleted."
