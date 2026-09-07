[CmdletBinding()]
param(
    [string]$EnvFile,
    [switch]$Online,
    [switch]$Help
)
$ErrorActionPreference = "Stop"
$WorkshopSrc = (Resolve-Path (Join-Path $PSScriptRoot "..")).Path
$WorkshopRoot = (Resolve-Path (Join-Path $WorkshopSrc "..")).Path
if ($Help) {
    Write-Host "Usage: ./preflight.ps1 [-EnvFile PATH] [-Online]"
    Write-Host "Read-only validation; -Online adds Azure catalog and quota checks."
    exit 0
}
if (-not $EnvFile) { $EnvFile = Join-Path $WorkshopRoot "sample.env" }
$EnvFile = (Resolve-Path $EnvFile).Path
foreach ($line in Get-Content $EnvFile) {
    if ($line -match '^\s*(#|$)') { continue }
    if ($line -notmatch '^([A-Za-z_][A-Za-z0-9_]*)=(.*)$') {
        throw "Invalid environment line: $line"
    }
    [Environment]::SetEnvironmentVariable($Matches[1], $Matches[2].Trim('"', "'"), "Process")
}

$failures = 0
foreach ($command in @("python3", "az", "azd")) {
    if (Get-Command $command -ErrorAction SilentlyContinue) {
        Write-Host "[OK] $command is installed."
    } else {
        Write-Warning "[ACTION] Install $command."
        $failures++
    }
}
$required = @(
    "AZURE_SUBSCRIPTION_ID", "AZURE_LOCATION", "AZURE_AI_DEPLOYMENTS_LOCATION",
    "CAMPAIGN_COORDINATOR_MODEL_NAME", "CAMPAIGN_COORDINATOR_MODEL_VERSION",
    "CAMPAIGN_COORDINATOR_MODEL_FORMAT", "CAMPAIGN_COORDINATOR_MODEL_SKU",
    "VISUAL_UNDERSTANDING_MODEL_NAME", "VISUAL_UNDERSTANDING_MODEL_VERSION",
    "VISUAL_UNDERSTANDING_MODEL_FORMAT", "VISUAL_UNDERSTANDING_MODEL_SKU",
    "CAMPAIGN_REASONING_MODEL_NAME", "CAMPAIGN_REASONING_MODEL_VERSION",
    "CAMPAIGN_REASONING_MODEL_FORMAT", "CAMPAIGN_REASONING_MODEL_SKU",
    "ADAPTIVE_COPY_MODEL_NAME", "ADAPTIVE_COPY_MODEL_VERSION",
    "ADAPTIVE_COPY_MODEL_FORMAT", "ADAPTIVE_COPY_MODEL_SKU",
    "MODEL_ROUTER_MODEL_NAME", "MODEL_ROUTER_MODEL_VERSION",
    "MODEL_ROUTER_MODEL_FORMAT", "MODEL_ROUTER_MODEL_SKU",
    "CREATIVE_IMAGE_MODEL_NAME", "CREATIVE_IMAGE_MODEL_VERSION",
    "CREATIVE_IMAGE_MODEL_FORMAT", "CREATIVE_IMAGE_MODEL_SKU"
)
foreach ($name in $required) {
    if (-not [Environment]::GetEnvironmentVariable($name, "Process")) {
        Write-Warning "[ACTION] Set $name."
        $failures++
    }
}
if (Get-Command python3 -ErrorAction SilentlyContinue) {
    & python3 (Join-Path $PSScriptRoot "validate-assets.py") --root $WorkshopSrc
    if ($LASTEXITCODE -ne 0) { $failures++ }
}
if ($Online -and $failures -eq 0) {
    & az account show --subscription $env:AZURE_SUBSCRIPTION_ID --output none
    if ($LASTEXITCODE -ne 0) { throw "[ACTION] Authenticate Azure CLI." }
    & azd auth login --check-status | Out-Null
    if ($LASTEXITCODE -ne 0) { throw "[ACTION] Authenticate azd with: azd auth login" }
    $env:CATALOG_JSON = & az cognitiveservices model list `
        --subscription $env:AZURE_SUBSCRIPTION_ID `
        --location $env:AZURE_AI_DEPLOYMENTS_LOCATION --output json
    & python3 (Join-Path $PSScriptRoot "verify-model-catalog.py")
    if ($LASTEXITCODE -ne 0) { throw "[ACTION] Model catalog verification failed." }
    & az cognitiveservices usage list `
        --subscription $env:AZURE_SUBSCRIPTION_ID `
        --location $env:AZURE_AI_DEPLOYMENTS_LOCATION `
        --query "[?currentValue < limit].{name:name.localizedValue,used:currentValue,limit:limit}" `
        --output table
    Write-Warning "[ACTION] Instructor: confirm capacity and partner Marketplace terms."
}
if ($failures -gt 0) { throw "Preflight found $failures blocking local issue(s)." }
Write-Host "[OK] Preflight completed without making changes."
