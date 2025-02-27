# PowerShell script to interact with Grok API using environment variables

# Load environment variables from .env file
$envFile = Join-Path $PSScriptRoot ".env"
if (Test-Path $envFile) {
    Get-Content $envFile | ForEach-Object {
        if ($_ -match '^([^#][^=]*)=(.*)$') {
            $name = $matches[1].Trim()
            $value = $matches[2].Trim()
            Set-Item -Path "env:$name" -Value $value
        }
    }
    Write-Host "Environment variables loaded from .env file" -ForegroundColor Green
} else {
    Write-Host "Warning: .env file not found at $envFile" -ForegroundColor Yellow
}

# Get API configuration from environment variables
$apiHost = if ($env:API_HOST) { $env:API_HOST } else { "127.0.0.1" }
$apiPort = if ($env:API_PORT) { $env:API_PORT } else { "8000" }
$modelName = if ($env:MODEL_NAME) { $env:MODEL_NAME } else { "grok-3" }
$sso = $env:GROK_SSO
$ssoRw = $env:GROK_SSO_RW

# Check if SSO tokens are available
if (-not $sso -or -not $ssoRw) {
    Write-Host "Error: SSO tokens not found in environment variables." -ForegroundColor Red
    Write-Host "Please make sure GROK_SSO and GROK_SSO_RW are set in your .env file." -ForegroundColor Red
    exit 1
}

# Function to make API calls
function Invoke-GrokAPI {
    param (
        [Parameter(Mandatory=$true)]
        [string]$Query,
        
        [Parameter(Mandatory=$false)]
        [switch]$Stream
    )
    
    # Prepare the API URL
    $apiUrl = "http://${apiHost}:${apiPort}/v1/chat/completions"
    
    # Prepare the headers with cookies
    $headers = @{
        "Content-Type" = "application/json"
        "Cookie" = "sso=${sso}; sso-rw=${ssoRw}"
    }
    
    # Prepare the request body
    $body = @{
        "model" = $modelName
        "messages" = @(
            @{
                "role" = "user"
                "content" = $Query
            }
        )
        "stream" = $Stream.IsPresent
    } | ConvertTo-Json
    
    Write-Host "Sending query to Grok API: $Query" -ForegroundColor Cyan
    
    try {
        if ($Stream) {
            # For streaming, we need to handle the response differently
            Write-Host "Streaming response:" -ForegroundColor Green
            $response = Invoke-WebRequest -Uri $apiUrl -Method POST -Headers $headers -Body $body -ResponseHeadersVariable responseHeaders
            $response.Content
        } else {
            # For non-streaming responses
            $response = Invoke-RestMethod -Uri $apiUrl -Method POST -Headers $headers -Body $body
            Write-Host "Response from Grok:" -ForegroundColor Green
            $response.choices[0].message.content
        }
    } catch {
        Write-Host "Error calling Grok API: $_" -ForegroundColor Red
        Write-Host "Status Code: $($_.Exception.Response.StatusCode.value__)" -ForegroundColor Red
        
        if ($_.ErrorDetails.Message) {
            Write-Host "Error Details: $($_.ErrorDetails.Message)" -ForegroundColor Red
        }
    }
}

# Example usage
Write-Host "=== Grok API PowerShell Example ===" -ForegroundColor Magenta
Write-Host "API Server: http://${apiHost}:${apiPort}" -ForegroundColor Magenta
Write-Host "Model: ${modelName}" -ForegroundColor Magenta
Write-Host 

# Get user input
$userQuery = Read-Host "Enter your question for Grok"

# Ask if streaming is desired
$streamResponse = Read-Host "Do you want a streaming response? (y/n)"
$useStream = $streamResponse -eq "y"

# Call the API
if ($useStream) {
    Invoke-GrokAPI -Query $userQuery -Stream
} else {
    Invoke-GrokAPI -Query $userQuery
}