<#
.SYNOPSIS
    Pause or resume the Fabric capacity created by this stack.

.DESCRIPTION
    A running F-SKU capacity bills by the hour whether or not anyone uses it.
    Pause it the moment the demo is over.

    Reads the capacity and resource group from the Terraform outputs, so there
    is nothing to hardcode.

.EXAMPLE
    .\scripts\capacity.ps1 pause
    .\scripts\capacity.ps1 resume
    .\scripts\capacity.ps1 status
#>
[CmdletBinding()]
param(
    [Parameter(Position = 0)]
    [ValidateSet('pause', 'resume', 'status')]
    [string]$Action = 'status',

    [string]$InfraDir = (Join-Path $PSScriptRoot '..\infra')
)

$ErrorActionPreference = 'Stop'

if (-not (az extension show --name microsoft-fabric 2>$null)) {
    Write-Host "Installing the 'microsoft-fabric' Azure CLI extension..."
    az extension add --name microsoft-fabric --only-show-errors
}

$resourceGroup = terraform -chdir=$InfraDir output -raw azure_resource_group
$capacity = terraform -chdir=$InfraDir output -raw fabric_capacity_name

switch ($Action) {
    'pause' {
        Write-Host "Pausing capacity '$capacity'..."
        az fabric capacity suspend --capacity-name $capacity --resource-group $resourceGroup
        Write-Host 'Paused. Fabric content on this capacity is unavailable until you resume.'
    }
    'resume' {
        Write-Host "Resuming capacity '$capacity'..."
        az fabric capacity resume --capacity-name $capacity --resource-group $resourceGroup
        Write-Host 'Resumed. Billing has restarted.'
    }
    'status' {
        az fabric capacity show --capacity-name $capacity --resource-group $resourceGroup `
            --query '{name:name, state:properties.state, sku:sku.name}' -o table
    }
}
