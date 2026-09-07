targetScope = 'resourceGroup'

param accountName string
param projectName string
param location string
param deployments array
param principalId string
param principalType string
param enableHostedAgents bool
param enableCapabilityHost bool
param applicationInsightsId string = ''

@secure()
param applicationInsightsConnectionString string = ''

param tags object = {}

resource account 'Microsoft.CognitiveServices/accounts@2025-06-01' = {
  name: accountName
  location: location
  tags: tags
  kind: 'AIServices'
  sku: {
    name: 'S0'
  }
  identity: {
    type: 'SystemAssigned'
  }
  properties: {
    allowProjectManagement: true
    customSubDomainName: accountName
    disableLocalAuth: true
    publicNetworkAccess: 'Enabled'
    networkAcls: {
      defaultAction: 'Allow'
      ipRules: []
      virtualNetworkRules: []
    }
  }

  @batchSize(1)
  resource modelDeployments 'deployments@2024-10-01' = [
    for deployment in deployments: {
      name: deployment.name
      sku: deployment.sku
      properties: {
        model: deployment.model
        versionUpgradeOption: 'OnceNewDefaultVersionAvailable'
      }
    }
  ]

  resource project 'projects' = {
    name: projectName
    location: location
    identity: {
      type: 'SystemAssigned'
    }
    properties: {
      displayName: 'Product Launch Studio'
      description: 'Model-selection and agent-optimization workshop project'
    }
    dependsOn: [
      modelDeployments
    ]
  }

  resource hostedAgentCapability 'capabilityHosts@2025-10-01-preview' = if (enableHostedAgents && enableCapabilityHost) {
    name: 'agents'
    properties: {
      capabilityHostKind: 'Agents'
      enablePublicHostingEnvironment: true
    }
  }
}

resource appInsightsConnection 'Microsoft.CognitiveServices/accounts/projects/connections@2025-04-01-preview' = if (!empty(applicationInsightsId)) {
  parent: account::project
  name: 'application-insights'
  properties: {
    category: 'AppInsights'
    target: applicationInsightsId
    authType: 'ApiKey'
    isSharedToAll: true
    credentials: {
      key: applicationInsightsConnectionString
    }
    metadata: {
      ApiType: 'Azure'
      ResourceId: applicationInsightsId
    }
  }
}

resource participantRole 'Microsoft.Authorization/roleAssignments@2022-04-01' = {
  scope: account::project
  name: guid(account::project.id, principalId, 'Azure AI User')
  properties: {
    principalId: principalId
    principalType: principalType
    roleDefinitionId: subscriptionResourceId(
      'Microsoft.Authorization/roleDefinitions',
      '53ca6127-db72-4b80-b1b0-d745d6d5456d'
    )
  }
}

output accountId string = account.id
output accountName string = account.name
output projectId string = account::project.id
output projectName string = account::project.name
output projectEndpoint string = account::project.properties.endpoints['AI Foundry API']
output openAIEndpoint string = account.properties.endpoints['OpenAI Language Model Instance API']
