targetScope = 'subscription'

@minLength(1)
@maxLength(64)
param environmentName string

@minLength(1)
@maxLength(90)
param resourceGroupName string = 'rg-${environmentName}'

param location string
param aiDeploymentsLocation string = location
param principalId string

@allowed([
  'User'
  'ServicePrincipal'
  'Group'
])
param principalType string = 'User'

param aiFoundryResourceName string = ''
param aiFoundryProjectName string = 'product-launch-studio'
param aiProjectDeploymentsJson string = '[]'
param enableHostedAgents bool = true
param enableCapabilityHost bool = false
param enableMonitoring bool = true

var tags = {
  'azd-env-name': environmentName
  workshop: 'from-model-selection-to-agent-optimization'
}
var token = uniqueString(subscription().id, environmentName, location)
var accountName = empty(aiFoundryResourceName) ? 'aif-${token}' : aiFoundryResourceName

resource resourceGroup 'Microsoft.Resources/resourceGroups@2024-03-01' = {
  name: resourceGroupName
  location: location
  tags: tags
}

module observability 'modules/observability.bicep' = if (enableMonitoring) {
  scope: resourceGroup
  name: 'observability'
  params: {
    location: location
    resourceToken: token
    tags: tags
  }
}

module foundry 'modules/foundry.bicep' = {
  scope: resourceGroup
  name: 'foundry'
  params: {
    accountName: accountName
    projectName: aiFoundryProjectName
    location: aiDeploymentsLocation
    deployments: json(aiProjectDeploymentsJson)
    principalId: principalId
    principalType: principalType
    enableHostedAgents: enableHostedAgents
    enableCapabilityHost: enableCapabilityHost
    applicationInsightsId: enableMonitoring ? observability!.outputs.applicationInsightsId : ''
    applicationInsightsConnectionString: enableMonitoring ? observability!.outputs.applicationInsightsConnectionString : ''
    tags: tags
  }
}

output AZURE_RESOURCE_GROUP string = resourceGroup.name
output AZURE_AI_ACCOUNT_ID string = foundry.outputs.accountId
output AZURE_AI_ACCOUNT_NAME string = foundry.outputs.accountName
output AZURE_AI_PROJECT_ID string = foundry.outputs.projectId
output AZURE_AI_FOUNDRY_PROJECT_ID string = foundry.outputs.projectId
output AZURE_AI_PROJECT_NAME string = foundry.outputs.projectName
output AZURE_AI_PROJECT_ENDPOINT string = foundry.outputs.projectEndpoint
output FOUNDRY_PROJECT_ENDPOINT string = foundry.outputs.projectEndpoint
output AZURE_OPENAI_ENDPOINT string = foundry.outputs.openAIEndpoint
output APPLICATIONINSIGHTS_RESOURCE_ID string = enableMonitoring ? observability!.outputs.applicationInsightsId : ''
output APPLICATIONINSIGHTS_CONNECTION_STRING string = enableMonitoring ? observability!.outputs.applicationInsightsConnectionString : ''
output LOG_ANALYTICS_WORKSPACE_ID string = enableMonitoring ? observability!.outputs.logAnalyticsWorkspaceId : ''
