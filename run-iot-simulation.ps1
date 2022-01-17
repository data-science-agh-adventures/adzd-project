param(
    [string]$dbName,
    [string]$containerName,
    [string]$resourceGroup,
    [string]$accountName,
    [Int]$nTestsToRun
)

$accountCheck = $(az cosmosdb show --resource-group $resourceGroup --name $accountName 2>$null)
if ($null -eq $accountCheck)
{
    Write-Output "Creating a new account..."
    $location = "westeurope"
    az cosmosdb create --resource-group $resourceGroup --name $accountName `
        --locations regionName=$location --output none
    Write-Output "Successfully added the account ${accountName}"
}

$dbCheck = $(az cosmosdb sql database show -a $accountName -g $resourceGroup -n $dbName 2>$null)
if ($null -eq $dbCheck)
{
    Write-Output "Creating a new database..."
    az cosmosdb sql database create -a $accountName -g $resourceGroup -n $dbName --output none
    Write-Output "Successfully create the database ${dbName}"
}

$containerCheck = $(az cosmosdb sql container show -a $accountName -g $resourceGroup -d $dbName -n $containerName 2>$null)
if ($null -eq $containerCheck)
{
    Write-Output "Creating a new container..."
    az cosmosdb sql container create -a $accountName -g $resourceGroup -d $dbName `
        -n $containerName -p "/dateTime" --output none
    Write-Output "Successfully created the container ${containerName}"
}

$outputsPath = "iot-simulation-latencies-${nTestsToRun}-nodes"
if (!(Test-Path $outputsPath))
{
    Write-Output "Creating an output directory for simulation measurings..."
    $_ = New-Item $outputsPath -ItemType "d"
}

$accountUri = $(az cosmosdb show --resource-group $resourceGroup --name $accountName --query documentEndpoint --output tsv)
$accountKey = $(az cosmosdb keys list --resource-group $resourceGroup --name $accountName --query primaryMasterKey --output tsv)

Write-Output "Starting ${nTestsToRun} IoT device emulators..."
$simulatorProcesses = 1..$nTestsToRun

foreach ($i in 1..$nTestsToRun)
{
    $simulatorProcesses[$i - 1] = $(Start-Process python -ArgumentList `
        "cosmosdb_iot_simulator.py --id ${i} --uri ${accountUri} --basedir ${outputsPath} --key ${accountKey} --db ${dbName} --cont ${containerName}" `
        -PassThru -NoNewWindow)
}

Write-Output "Press any key to stop simulation"
$_ = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")

foreach ($simProcess in $simulatorProcesses)
{
    # Write-Output $simProcess
    $_ = $simProcess.Kill()
}
# Write-Output "Account URI: ${accountUri}"
# Write-Output "Account key: ${accountKey}"