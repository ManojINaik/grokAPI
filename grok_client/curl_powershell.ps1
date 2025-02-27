# PowerShell script to make a direct curl-like request to Grok API using environment variables

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
    exit 1
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

# Display configuration
Write-Host "=== Grok API Direct Request Example ===" -ForegroundColor Magenta
Write-Host "API Server: http://${apiHost}:${apiPort}" -ForegroundColor Magenta
Write-Host "Model: ${modelName}" -ForegroundColor Magenta
Write-Host 

# Get user input
$userQuery = Read-Host "Enter your question for Grok"

# Ask if streaming is desired
$streamResponse = Read-Host "Do you want a streaming response? (y/n)"
$useStream = $streamResponse -eq "y"

# Prepare the API URL
$apiUrl = "http://${apiHost}:${apiPort}/v1/chat/completions"

# Prepare the cookie string
$cookieString = "sso=${sso}; sso-rw=${ssoRw}"

# Prepare the request body
$bodyObj = @{
    "model" = $modelName
    "messages" = @(
        @{
            "role" = "user"
            "content" = $userQuery
        }
    )
}

# Add stream parameter if requested
if ($useStream) {
    $bodyObj.Add("stream", $true)
    Write-Host "Sending streaming request to Grok API..." -ForegroundColor Cyan
} else {
    Write-Host "Sending request to Grok API..." -ForegroundColor Cyan
}

$bodyJson = ConvertTo-Json $bodyObj

# Make the direct curl-like request
Write-Host "Executing request with the following parameters:" -ForegroundColor Yellow
Write-Host "URL: $apiUrl" -ForegroundColor Yellow
Write-Host "Cookie: $cookieString" -ForegroundColor Yellow
Write-Host "Body: $bodyJson" -ForegroundColor Yellow
Write-Host 

try {
    # Execute the request using Invoke-WebRequest (PowerShell's curl equivalent)
    # Create a WebSession object to properly handle cookies
    $session = New-Object Microsoft.PowerShell.Commands.WebRequestSession
    
    # Add the SSO cookies to the session
    $cookie1 = New-Object System.Net.Cookie
    $cookie1.Name = "sso"
    $cookie1.Value = $sso
    $cookie1.Domain = $apiHost
    $session.Cookies.Add($cookie1)
    
    $cookie2 = New-Object System.Net.Cookie
    $cookie2.Name = "sso-rw"
    $cookie2.Value = $ssoRw
    $cookie2.Domain = $apiHost
    $session.Cookies.Add($cookie2)
    
    # Make the request with the session
    $response = Invoke-WebRequest -Uri $apiUrl -Method POST -Headers @{
        "Content-Type" = "application/json"
    } -WebSession $session -Body $bodyJson -UseBasicParsing
    
    Write-Host "Response from Grok:" -ForegroundColor Green
    $response.Content
} catch {
    Write-Host "Error calling Grok API: $_" -ForegroundColor Red
    Write-Host "Status Code: $($_.Exception.Response.StatusCode.value__)" -ForegroundColor Red
    
    if ($_.ErrorDetails.Message) {
        Write-Host "Error Details: $($_.ErrorDetails.Message)" -ForegroundColor Red
    }
}