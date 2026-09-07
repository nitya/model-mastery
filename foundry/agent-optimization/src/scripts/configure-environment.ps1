[CmdletBinding()]
param(
    [Parameter(Mandatory = $false)][string]$EnvFile,
    [switch]$Apply,
    [switch]$Yes,
    [switch]$Help
)
$ErrorActionPreference = "Stop"
$WorkshopSrc = (Resolve-Path (Join-Path $PSScriptRoot "..")).Path
if ($Help) {
    Write-Host "Usage: ./configure-environment.ps1 -EnvFile PATH [-Apply] [-Yes]"
    Write-Host "Default is a preview. -Apply only updates local azd environment state."
    exit 0
}
if (-not $EnvFile) { throw "-EnvFile is required. Use -Help for usage." }
foreach ($line in Get-Content (Resolve-Path $EnvFile)) {
    if ($line -match '^\s*(#|$)') { continue }
    if ($line -notmatch '^([A-Za-z_][A-Za-z0-9_]*)=(.*)$') { throw "Invalid environment line: $line" }
    [Environment]::SetEnvironmentVariable($Matches[1], $Matches[2].Trim('"', "'"), "Process")
}
$keys = @(
    "AZURE_SUBSCRIPTION_ID", "AZURE_LOCATION", "AZURE_AI_DEPLOYMENTS_LOCATION",
    "AZURE_RESOURCE_GROUP", "AZURE_AI_ACCOUNT_NAME", "AZURE_AI_PROJECT_NAME",
    "ENABLE_HOSTED_AGENTS", "ENABLE_CAPABILITY_HOST", "AZD_AGENT_SKIP_ACR", "ENABLE_MONITORING",
    "COPYWRITER_DEPLOYMENT_MODE",
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
if (-not $env:AZURE_ENV_NAME) { throw "AZURE_ENV_NAME is required." }
foreach ($key in $keys) {
    $value = [Environment]::GetEnvironmentVariable($key, "Process")
    if ($value) { Write-Host "azd env set $key `"$value`"" }
}
if (-not $Apply) { Write-Host "[OK] Preview only; no state changed."; exit 0 }
if (-not $Yes -and (Read-Host "Type CONFIGURE to update local azd state") -ne "CONFIGURE") {
    throw "Cancelled."
}
Push-Location $WorkshopSrc
try {
    & azd env new $env:AZURE_ENV_NAME --no-prompt 2>$null
    if ($LASTEXITCODE -ne 0) { & azd env select $env:AZURE_ENV_NAME }
    foreach ($key in $keys) {
        $value = [Environment]::GetEnvironmentVariable($key, "Process")
        if ($value) { & azd env set $key $value }
    }
    if (-not $env:AZURE_PRINCIPAL_ID) {
        $principal = & az ad signed-in-user show --query id --output tsv
        if ($LASTEXITCODE -eq 0 -and $principal) {
            & azd env set AZURE_PRINCIPAL_ID $principal
            & azd env set AZURE_PRINCIPAL_TYPE User
        }
    }
} finally { Pop-Location }
Write-Host "[OK] Local azd environment configured; Azure was not provisioned."
