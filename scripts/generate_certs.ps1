#!/usr/bin/env pwsh

<#
.SYNOPSIS
    Generate SSL certificates using mkcert for local development
.DESCRIPTION
    Creates SSL certificates for localhost, agentc.local, host.docker.internal,
    and the current machine's hostname using mkcert
#>

$scriptPath = Split-Path -Parent $MyInvocation.MyCommand.Path
$projectRoot = Split-Path -Parent $scriptPath
Set-Location $projectRoot

# Get the machine's hostname
$hostname = $env:COMPUTERNAME
if ([string]::IsNullOrEmpty($hostname)) {
    $hostname = hostname
}

Write-Host "Generating certificates for:" -ForegroundColor Cyan
Write-Host "  - localhost" -ForegroundColor Green
Write-Host "  - agentc.local" -ForegroundColor Green
Write-Host "  - host.docker.internal" -ForegroundColor Green
Write-Host "  - $hostname" -ForegroundColor Green

# Generate the certificates
try {
    .\build_support\mkcert -install
    .\build_support\mkcert -cert-file agent_c_config\certs\cert.pem -key-file agent_c_config\certs\key.pem localhost agentc.local host.docker.internal $hostname

    if ($LASTEXITCODE -eq 0) {
        Write-Host "`nCertificates generated successfully!" -ForegroundColor Green
    } else {
        Write-Error "mkcert command failed with exit code: $LASTEXITCODE"
        exit $LASTEXITCODE
    }
} catch {
    Write-Error "Failed to generate certificates: $_"
    exit 1
}