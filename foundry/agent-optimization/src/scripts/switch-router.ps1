[CmdletBinding()]
param(
    [Parameter(Mandatory = $false)][string]$EnvFile,
    [switch]$Offline,
    [switch]$Apply,
    [switch]$Yes,
    [switch]$Help
)
$ErrorActionPreference = "Stop"
$WorkshopSrc = (Resolve-Path (Join-Path $PSScriptRoot "..")).Path
if ($Help) {
    Write-Host "Usage: ./switch-router.ps1 -EnvFile PATH [-Offline|-Apply] [-Yes]"
    Write-Host "Default runs azd what-if; -Offline only prints; -Apply requires confirmation."
    exit 0
}
if (-not $EnvFile) { throw "-EnvFile is required. Use -Help for usage." }
foreach ($line in Get-Content (Resolve-Path $EnvFile)) {
    if ($line -match '^\s*(#|$)') { continue }
    if ($line -notmatch '^([A-Za-z_][A-Za-z0-9_]*)=(.*)$') { throw "Invalid environment line: $line" }
    [Environment]::SetEnvironmentVariable($Matches[1], $Matches[2].Trim('"', "'"), "Process")
}
foreach ($name in @("MODEL_ROUTER_MODEL_NAME", "MODEL_ROUTER_MODEL_VERSION", "MODEL_ROUTER_MODEL_FORMAT", "MODEL_ROUTER_MODEL_SKU")) {
    if (-not [Environment]::GetEnvironmentVariable($name, "Process")) { throw "$name is required." }
}
Write-Host "Deployment: adaptive-copy"
Write-Host "Current: $env:ADAPTIVE_COPY_MODEL_FORMAT/$env:ADAPTIVE_COPY_MODEL_NAME/$env:ADAPTIVE_COPY_MODEL_VERSION"
Write-Host "New:     $env:MODEL_ROUTER_MODEL_FORMAT/$env:MODEL_ROUTER_MODEL_NAME/$env:MODEL_ROUTER_MODEL_VERSION"
if ($Offline) { Write-Host "[OK] Offline preview only; no state changed."; exit 0 }
& (Join-Path $PSScriptRoot "preflight.ps1") -EnvFile $EnvFile -Online
if ($LASTEXITCODE -ne 0) { throw "Preflight failed." }
Push-Location $WorkshopSrc
try {
    if (-not $Apply) {
        $env:ADAPTIVE_COPY_MODEL_NAME = $env:MODEL_ROUTER_MODEL_NAME
        $env:ADAPTIVE_COPY_MODEL_VERSION = $env:MODEL_ROUTER_MODEL_VERSION
        $env:ADAPTIVE_COPY_MODEL_FORMAT = $env:MODEL_ROUTER_MODEL_FORMAT
        $env:ADAPTIVE_COPY_MODEL_SKU = $env:MODEL_ROUTER_MODEL_SKU
        $env:COPYWRITER_DEPLOYMENT_MODE = "routed"
        & azd provision --preview --no-prompt
        if ($LASTEXITCODE -ne 0) { throw "What-if failed." }
        Write-Host "[OK] What-if complete; no deployment changed."
        exit 0
    }
    if (-not $Yes -and (Read-Host "Type SWITCH to remap adaptive-copy") -ne "SWITCH") {
        throw "Cancelled."
    }
    & azd env set ADAPTIVE_COPY_MODEL_NAME $env:MODEL_ROUTER_MODEL_NAME
    & azd env set ADAPTIVE_COPY_MODEL_VERSION $env:MODEL_ROUTER_MODEL_VERSION
    & azd env set ADAPTIVE_COPY_MODEL_FORMAT $env:MODEL_ROUTER_MODEL_FORMAT
    & azd env set ADAPTIVE_COPY_MODEL_SKU $env:MODEL_ROUTER_MODEL_SKU
    & azd env set COPYWRITER_DEPLOYMENT_MODE routed
    & azd provision --no-prompt
    if ($LASTEXITCODE -ne 0) { throw "Router switch failed." }
} finally { Pop-Location }
Write-Host "[OK] adaptive-copy now maps to Model Router."
