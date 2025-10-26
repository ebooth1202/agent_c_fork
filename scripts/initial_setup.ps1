#Requires -Version 5.1

<#
.SYNOPSIS
    Initial setup script for Agent C project on Windows
.DESCRIPTION
    This script handles all prerequisites and initial setup for the Agent C project:
    - Installs required tools via winget (Python, git, MSVC build tools, Node.js, FFmpeg)
    - Installs Rust via Chocolatey
    - Creates Python virtual environment
    - Copies configuration files from examples
    - Installs npm/pnpm/lerna dependencies
    - Builds TypeScript SDK
    - Installs Python dependencies
.NOTES
    Requirements:
    - Windows 10 or later
    - Winget (Windows Package Manager) must be installed
    - Internet connection for downloading packages
#>

[CmdletBinding()]
param(
    [switch]$NoElevate  # Skip auto-elevation if user wants to run without admin
)

# Set error action preference
$ErrorActionPreference = "Stop"
$ProgressPreference = "SilentlyContinue"  # Speeds up downloads

# ANSI color codes for better output
$ColorReset = "`e[0m"
$ColorGreen = "`e[32m"
$ColorYellow = "`e[33m"
$ColorRed = "`e[31m"
$ColorCyan = "`e[36m"
$ColorBold = "`e[1m"

# Helper Functions
function Write-ColorOutput {
    param(
        [string]$Message,
        [string]$Color = $ColorReset,
        [switch]$NoNewline
    )
    if ($NoNewline) {
        Write-Host "${Color}${Message}${ColorReset}" -NoNewline
    } else {
        Write-Host "${Color}${Message}${ColorReset}"
    }
}

function Write-Success {
    param([string]$Message)
    Write-ColorOutput "✓ $Message" -Color $ColorGreen
}

function Write-Info {
    param([string]$Message)
    Write-ColorOutput "ℹ $Message" -Color $ColorCyan
}

function Write-Warning {
    param([string]$Message)
    Write-ColorOutput "⚠ $Message" -Color $ColorYellow
}

function Write-Error {
    param([string]$Message)
    Write-ColorOutput "✗ $Message" -Color $ColorRed
}

function Write-Header {
    param([string]$Message)
    Write-Host ""
    Write-ColorOutput "═══════════════════════════════════════════════════════════════" -Color $ColorBold
    Write-ColorOutput "  $Message" -Color $ColorBold
    Write-ColorOutput "═══════════════════════════════════════════════════════════════" -Color $ColorBold
    Write-Host ""
}

function Test-CommandExists {
    param([string]$Command)
    $null = Get-Command $Command -ErrorAction SilentlyContinue
    return $?
}

function Test-IsAdministrator {
    $currentPrincipal = New-Object Security.Principal.WindowsPrincipal([Security.Principal.WindowsIdentity]::GetCurrent())
    return $currentPrincipal.IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)
}

function Refresh-EnvironmentPath {
    $env:Path = [System.Environment]::GetEnvironmentVariable("Path", "Machine") + ";" + 
                [System.Environment]::GetEnvironmentVariable("Path", "User")
}

# Main Script Start
Write-Header "Agent C Initial Setup Script"

# 1. Set working directory to project root (parent of scripts folder)
$scriptPath = Split-Path -Parent $MyInvocation.MyCommand.Path
$projectRoot = Split-Path -Parent $scriptPath
Set-Location $projectRoot
Write-Success "Working directory set to: $projectRoot"

# Check for administrator privileges and auto-elevate if needed
if (-not (Test-IsAdministrator)) {
    if ($NoElevate) {
        Write-Warning "Running without administrator privileges (-NoElevate specified)"
        Write-Warning "Some installations may fail without elevation."
        Write-Host ""
    } else {
        Write-Info "Administrator privileges required for installations."
        Write-Info "Attempting to elevate..."
        
        try {
            # Build argument list
            $arguments = "-NoProfile -ExecutionPolicy Bypass -File `"$($MyInvocation.MyCommand.Path)`""
            
            # Add -NoElevate to prevent infinite loop if elevation fails
            $arguments += " -NoElevate"
            
            # Start elevated process
            Start-Process PowerShell.exe -ArgumentList $arguments -Verb RunAs -WorkingDirectory $projectRoot
            
            # Exit current non-elevated process
            Write-Info "Launching elevated process..."
            exit 0
        } catch {
            Write-Warning "Failed to elevate privileges: $_"
            Write-Warning "Continuing without administrator privileges."
            Write-Warning "Some installations may fail."
            Write-Host ""
        }
    }
} else {
    Write-Success "Running with administrator privileges"
}

# 2. Check for winget
Write-Header "Checking Prerequisites"
Write-Info "Checking for Windows Package Manager (winget)..."

if (-not (Test-CommandExists "winget")) {
    Write-Warning "Winget is not installed!"
    Write-Info "Opening Microsoft Store to install Windows Package Manager..."
    Write-Info "Please install it and then re-run this script."
    
    # Open MS Store to winget page
    Start-Process "ms-windows-store://pdp?hl=en-us&gl=us&productid=9nblggh4nns1&mode=full&referrer=storeforweb&source=https%3A%2F%2Fgithub.com%2F&webid=6753df9e-d22b-47f0-bba2-c0ce73e53a57&websessionid=e8508469-3fde-4884-bda1-be9b8d4c2495"
    
    Write-Host ""
    Write-Info "Press any key to exit after installing winget..."
    $null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
    exit 1
}

Write-Success "Winget is installed"

# 3. Check for Git
Write-Info "Checking for Git..."
if (-not (Test-CommandExists "git")) {
    Write-Warning "Git is not installed. Installing..."
    try {
        winget install --id Git.Git -e --accept-source-agreements --accept-package-agreements --silent
        Refresh-EnvironmentPath
        Write-Success "Git installed successfully"
    } catch {
        Write-Error "Failed to install Git: $_"
        exit 1
    }
} else {
    $gitVersion = git --version
    Write-Success "Git is already installed: $gitVersion"
}

# 4. Check for Python 3.12.x
Write-Info "Checking for Python 3.12.x..."
$pythonInstalled = $false
$pythonVersion = $null

if (Test-CommandExists "python") {
    try {
        $pythonVersion = python --version 2>&1
        if ($pythonVersion -match "Python 3\.12\.") {
            $pythonInstalled = $true
            Write-Success "Python 3.12.x is already installed: $pythonVersion"
        } else {
            Write-Warning "Python is installed but not version 3.12.x: $pythonVersion"
        }
    } catch {
        Write-Warning "Could not determine Python version"
    }
}

if (-not $pythonInstalled) {
    Write-Warning "Python 3.12.x is not installed. Installing..."
    try {
        winget install Python.Python.3.12 --accept-source-agreements --accept-package-agreements --silent
        Refresh-EnvironmentPath
        Write-Success "Python 3.12 installed successfully"
    } catch {
        Write-Error "Failed to install Python: $_"
        exit 1
    }
}

# 5. Check for/Create Python virtual environment
Write-Header "Setting Up Python Environment"
Write-Info "Checking for Python virtual environment..."

if (Test-Path ".venv") {
    Write-Success "Virtual environment already exists"
} else {
    Write-Info "Creating Python virtual environment..."
    try {
        python -m venv .venv
        Write-Success "Virtual environment created successfully"
    } catch {
        Write-Error "Failed to create virtual environment: $_"
        exit 1
    }
}

# 6. Check for MSVC Build Tools
Write-Header "Checking Development Tools"
Write-Info "Checking for Visual Studio Build Tools..."

# Check for cl.exe in common locations or via vswhere
$vswhereExists = Test-Path "${env:ProgramFiles(x86)}\Microsoft Visual Studio\Installer\vswhere.exe"
$buildToolsInstalled = $false

if ($vswhereExists) {
    $vsPath = & "${env:ProgramFiles(x86)}\Microsoft Visual Studio\Installer\vswhere.exe" -latest -products * -requires Microsoft.VisualStudio.Component.VC.Tools.x86.x64 -property installationPath 2>$null
    if ($vsPath) {
        $buildToolsInstalled = $true
        Write-Success "Visual Studio Build Tools are already installed"
    }
}

if (-not $buildToolsInstalled) {
    Write-Warning "Visual Studio Build Tools not found. Installing..."
    Write-Info "This may take several minutes..."
    try {
        winget install Microsoft.VisualStudio.2022.BuildTools --accept-source-agreements --accept-package-agreements --silent --override "--quiet --wait --add Microsoft.VisualStudio.Workload.VCTools --includeRecommended"
        Write-Success "Visual Studio Build Tools installed successfully"
    } catch {
        Write-Error "Failed to install Visual Studio Build Tools: $_"
        Write-Warning "You may need to install this manually"
    }
}

# 7. Check for Node.js
Write-Info "Checking for Node.js..."
if (-not (Test-CommandExists "node")) {
    Write-Warning "Node.js is not installed. Installing..."
    try {
        winget install --id=OpenJS.NodeJS -e --accept-source-agreements --accept-package-agreements --silent
        Refresh-EnvironmentPath
        Write-Success "Node.js installed successfully"
    } catch {
        Write-Error "Failed to install Node.js: $_"
        exit 1
    }
} else {
    $nodeVersion = node --version
    Write-Success "Node.js is already installed: $nodeVersion"
}

# 8. Check for FFmpeg
Write-Info "Checking for FFmpeg..."
if (-not (Test-CommandExists "ffmpeg")) {
    Write-Warning "FFmpeg is not installed. Installing..."
    try {
        winget install --id=Gyan.FFmpeg -e --accept-source-agreements --accept-package-agreements --silent
        Refresh-EnvironmentPath
        Write-Success "FFmpeg installed successfully"
    } catch {
        Write-Error "Failed to install FFmpeg: $_"
        Write-Warning "You may need to install this manually"
    }
} else {
    $ffmpegVersion = ffmpeg -version 2>&1 | Select-Object -First 1
    Write-Success "FFmpeg is already installed"
}

# 9. Check for Rust (via Chocolatey)
Write-Info "Checking for Rust..."
if (-not (Test-CommandExists "rustc")) {
    Write-Warning "Rust is not installed. Installing via Chocolatey..."
    
    # Check for Chocolatey
    if (-not (Test-CommandExists "choco")) {
        Write-Info "Chocolatey is not installed. Installing..."
        try {
            winget install Chocolatey.Chocolatey --accept-source-agreements --accept-package-agreements --silent
            Refresh-EnvironmentPath
            Write-Success "Chocolatey installed successfully"
        } catch {
            Write-Error "Failed to install Chocolatey: $_"
            Write-Warning "Skipping Rust installation"
        }
    } else {
        Write-Success "Chocolatey is already installed"
    }
    
    # Install Rust if Chocolatey is now available
    if (Test-CommandExists "choco") {
        Write-Info "Installing Rust via Chocolatey..."
        try {
            choco install rust -y
            Refresh-EnvironmentPath
            Write-Success "Rust installed successfully"
        } catch {
            Write-Error "Failed to install Rust: $_"
            Write-Warning "You may need to install this manually"
        }
    }
} else {
    $rustVersion = rustc --version
    Write-Success "Rust is already installed: $rustVersion"
}

# 10. Configuration Files Setup
Write-Header "Setting Up Configuration Files"

# Copy .env file
if (Test-Path ".env") {
    Write-Success "Config file (.env) already exists"
} else {
    if (Test-Path "example.env") {
        Write-Info "Copying example.env to .env..."
        Copy-Item "example.env" ".env"
        Write-Success "Created .env file"
        Write-Warning "Please edit the .env file to configure your API keys"
        
        # Open in default text editor
        Write-Info "Opening .env in editor..."
        notepad.exe .env
    } else {
        Write-Warning "example.env not found, skipping .env creation"
    }
}

# Copy local workspaces config
if (Test-Path ".local_workspaces.json") {
    Write-Success "Local workspaces config already exists"
} else {
    if (Test-Path "local_workspaces.example.json") {
        Write-Info "Creating local workspaces config..."
        Copy-Item "local_workspaces.example.json" ".local_workspaces.json"
        Write-Success "Created .local_workspaces.json"
    } else {
        Write-Warning "local_workspaces.example.json not found, skipping"
    }
}

# Copy demo .env.local
$demoEnvPath = "src\typescript_client_sdk\packages\demo\.env.local"
$demoEnvExample = "src\typescript_client_sdk\packages\demo\.env.example"
if (Test-Path $demoEnvPath) {
    Write-Success "Demo config already exists"
} else {
    if (Test-Path $demoEnvExample) {
        Write-Info "Creating demo config..."
        Copy-Item $demoEnvExample $demoEnvPath
        Write-Success "Created demo .env.local"
    } else {
        Write-Warning "Demo .env.example not found, skipping"
    }
}

# 11. Activate virtual environment and install Python dependencies
Write-Header "Installing Python Dependencies"

Write-Info "Activating virtual environment..."
$activateScript = Join-Path $projectRoot ".venv\Scripts\Activate.ps1"

if (Test-Path $activateScript) {
    try {
        & $activateScript
        Write-Success "Virtual environment activated"
        
        # Upgrade pip
        Write-Info "Upgrading pip..."
        python -m pip install --upgrade pip --quiet
        Write-Success "Pip upgraded"
        
        # Install tomli
        Write-Info "Installing tomli..."
        pip install tomli --quiet
        Write-Success "tomli installed"
        
    } catch {
        Write-Error "Failed to activate virtual environment: $_"
        Write-Warning "You may need to set execution policy: Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser"
        exit 1
    }
} else {
    Write-Error "Virtual environment activation script not found at: $activateScript"
    exit 1
}

# 12. Configure npm and install global packages
Write-Header "Installing Node.js Global Packages"

Write-Info "Configuring npm for faster installs..."
npm config set audit false
npm config set fund false
npm config set fetch-retries 0
npm config set progress false
Write-Success "npm configured"

Write-Info "Installing pnpm globally..."
try {
    npm install -g pnpm@10 --no-audit --no-fund --silent
    Write-Success "pnpm installed"
} catch {
    Write-Error "Failed to install pnpm: $_"
    exit 1
}

Write-Info "Installing lerna globally..."
try {
    $env:npm_config_ignore_scripts = "true"
    npm install -g "lerna@^9" --no-audit --no-fund --silent
    Remove-Item Env:\npm_config_ignore_scripts
    Write-Success "lerna installed"
} catch {
    Write-Error "Failed to install lerna: $_"
    exit 1
}

# 13. Install TypeScript Client SDK dependencies
Write-Header "Building TypeScript Client SDK"

$sdkPath = "src\typescript_client_sdk"
if (Test-Path $sdkPath) {
    Write-Info "Installing TypeScript Client SDK dependencies..."
    try {
        pnpm install --dir $sdkPath
        Write-Success "SDK dependencies installed"
        
        Write-Info "Building TypeScript Client SDK..."
        pnpm --dir $sdkPath build
        Write-Success "SDK built successfully"
    } catch {
        Write-Error "Failed to build TypeScript SDK: $_"
        exit 1
    }
} else {
    Write-Warning "TypeScript SDK path not found, skipping SDK setup"
}

# 14. Install Python backend dependencies
Write-Header "Installing Python Backend Dependencies"

$installDepsScript = Join-Path $scriptPath "install_deps.bat"
if (Test-Path $installDepsScript) {
    Write-Info "Installing Python backend dependencies..."
    try {
        & cmd /c $installDepsScript
        Write-Success "Python dependencies installed"
    } catch {
        Write-Error "Failed to install Python dependencies: $_"
        exit 1
    }
} else {
    Write-Warning "install_deps.bat not found at: $installDepsScript"
}

# Final Summary
Write-Header "Setup Complete!"

Write-Success "Initial setup completed successfully!"
Write-Host ""
Write-Info "Next steps:"
Write-ColorOutput "  1. Review and update .env file with your API keys" -Color $ColorYellow
Write-ColorOutput "  2. Activate the virtual environment:" -Color $ColorCyan
Write-ColorOutput "     .venv\Scripts\Activate.ps1" -Color $ColorCyan
Write-ColorOutput "  3. Start working on the project!" -Color $ColorGreen
Write-Host ""
Write-Warning "If you installed new tools, you may need to restart your terminal or computer"
Write-Warning "for PATH changes to take full effect."
Write-Host ""
