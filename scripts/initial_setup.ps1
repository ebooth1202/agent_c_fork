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
$ColorReset = "$([char]27)[0m"
$ColorGreen = "$([char]27)[32m"
$ColorYellow = "$([char]27)[33m"
$ColorRed = "$([char]27)[31m"
$ColorCyan = "$([char]27)[36m"
$ColorBold = "$([char]27)[1m"

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

function Show-Success {
    param([string]$Message)
    Write-ColorOutput " $Message" -Color $ColorGreen
}

function Show-Info {
    param([string]$Message)
    Write-ColorOutput "$Message" -Color $ColorCyan
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
    Write-ColorOutput "===============================================================" -Color $ColorBold
    Write-ColorOutput "  $Message" -Color $ColorBold
    Write-ColorOutput "===============================================================" -Color $ColorBold
    Write-Host ""
}

function Test-CommandExists {
    param([string]$Command)
    $null = Get-Command $Command -ErrorAction SilentlyContinue
    return $?
}

function Refresh-EnvironmentPath {
    $env:Path = [System.Environment]::GetEnvironmentVariable("Path", "Machine") + ";" + [System.Environment]::GetEnvironmentVariable("Path", "User")
}


function Test-IsAdministrator {
    $currentPrincipal = New-Object Security.Principal.WindowsPrincipal([Security.Principal.WindowsIdentity]::GetCurrent())
    return $currentPrincipal.IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)
}



# Main Script Start
Write-Header "Agent C Initial Setup Script"

# 1. Set working directory to project root (parent of scripts folder)
$scriptPath = Split-Path -Parent $MyInvocation.MyCommand.Path
$projectRoot = Split-Path -Parent $scriptPath
Set-Location $projectRoot
Show-Success "Working directory set to: $projectRoot"
#scripts\generate_drive_mappings.ps1
# Check for administrator privileges and auto-elevate if needed
if (-not (Test-IsAdministrator)) {
    if ($NoElevate) {
        Write-Warning "Running without administrator privileges (-NoElevate specified)"
        Write-Warning "Some installations may fail without elevation."
        Write-Host ""
    } else {
        Show-Success "Administrator privileges required for installations."
        Show-Info "Attempting to elevate..."

        try {
            # Build argument list
            $arguments = "-ExecutionPolicy Bypass -File `"$($MyInvocation.MyCommand.Path)`""

            # Add -NoElevate to prevent infinite loop if elevation fails
            $arguments += " -NoElevate"

            # Start elevated process
            Start-Process PowerShell.exe -ArgumentList $arguments -Verb RunAs -WorkingDirectory $projectRoot

            # Exit current non-elevated process
            Show-Info "Launching elevated process..."
            exit 0
        } catch {
            Write-Warning "Failed to elevate privileges: $_"
            Write-Warning "Continuing without administrator privileges."
            Write-Warning "Some installations may fail."
            Write-Host ""
        }
    }
} else {
    Show-Success "Running with administrator privileges"
}

# 2. Check for winget
Write-Header "Checking Prerequisites"
Show-Info "Checking for Windows Package Manager (winget)..."

if (-not (Test-CommandExists "winget")) {
    Write-Warning "Winget is not installed!"
    Show-Info "Open the Microsoft Store to install Windows Package Manager..."
    Show-Info "Please install it and then re-run this script."

    # Open MS Store to winget page

    Write-Host ""
    Show-Info "Press any key to exit after installing winget..."
    $null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
    exit 1
}

Show-Success "Winget is installed"

# 3. Check for Git
Show-Info "Checking for Git..."
if (-not (Test-CommandExists "git")) {
    Write-Warning "Git is not installed. Installing..."
    try {
        winget install --id Git.Git -e --accept-source-agreements --accept-package-agreements --silent
        Refresh-EnvironmentPath
        Show-Success "Git installed successfully"
    } catch {
        Write-Error "Failed to install Git: $_"
        exit 1
    }
} else {
    $gitVersion = git --version
    Show-Success "Git is already installed: $gitVersion"
}

# 4. Check for Python 3.12.x
Show-Info "Checking for Python 3.12.x..."
$pythonInstalled = $false
$pythonVersion = $null

if (Test-CommandExists "python") {
    try {
        $pythonVersion = python --version 2>&1
        if ($pythonVersion -match "Python 3\.12\.") {
            $pythonInstalled = $true
            Show-Success "Python 3.12.x is already installed: $pythonVersion"
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
        Show-Success "Python 3.12 installed successfully"
    } catch {
        Write-Error "Failed to install Python: $_"
        exit 1
    }
}

# 5. Check for/Create Python virtual environment
Write-Header "Setting Up Python Environment"
Show-Info "Checking for Python virtual environment..."

if (Test-Path ".venv") {
    Show-Success "Virtual environment already exists"
} else {
    Show-Info "Creating Python virtual environment..."
    try {
        python -m venv .venv
        Show-Success "Virtual environment created successfully"
    } catch {
        Write-Error "Failed to create virtual environment: $_"
        exit 1
    }
}

# 6. Check for MSVC Build Tools
Write-Header "Checking Development Tools"
Show-Info "Checking for Visual Studio Build Tools..."

# Check for cl.exe in common locations or via vswhere
$vswhereExists = Test-Path "${env:ProgramFiles(x86)}\Microsoft Visual Studio\Installer\vswhere.exe"
$buildToolsInstalled = $false

if ($vswhereExists) {
    $vsPath = & "${env:ProgramFiles(x86)}\Microsoft Visual Studio\Installer\vswhere.exe" -latest -products * -requires Microsoft.VisualStudio.Component.VC.Tools.x86.x64 -property installationPath 2>$null
    if ($vsPath) {
        $buildToolsInstalled = $true
        Show-Success "Visual Studio Build Tools are already installed"
    }
}

if (-not $buildToolsInstalled) {
    Write-Warning "Visual Studio Build Tools not found. Installing..."
    Show-Info "This may take several minutes..."
    try {
        winget install Microsoft.VisualStudio.2022.BuildTools --accept-source-agreements --accept-package-agreements --silent --override "--quiet --wait --add Microsoft.VisualStudio.Workload.VCTools --includeRecommended"
        Show-Success "Visual Studio Build Tools installed successfully"
    } catch {
        Write-Error "Failed to install Visual Studio Build Tools: $_"
        Write-Warning "You may need to install this manually"
    }
}

# 7. Check for Node.js
Show-Info "Checking for Node.js..."
if (-not (Test-CommandExists "node")) {
    Write-Warning "Node.js is not installed. Installing..."
    try {
        winget install --id=OpenJS.NodeJS -e --accept-source-agreements --accept-package-agreements --silent
        Refresh-EnvironmentPath
        Show-Success "Node.js installed successfully"
    } catch {
        Write-Error "Failed to install Node.js: $_"
        exit 1
    }
} else {
    $nodeVersion = node --version
    Show-Success "Node.js is already installed: $nodeVersion"
}

# 8. Check for FFmpeg
Show-Info "Checking for FFmpeg..."
if (-not (Test-CommandExists "ffmpeg")) {
    Write-Warning "FFmpeg is not installed. Installing..."
    try {
        winget install --id=Gyan.FFmpeg -e --accept-source-agreements --accept-package-agreements --silent
        Refresh-EnvironmentPath
        Show-Success "FFmpeg installed successfully"
    } catch {
        Write-Error "Failed to install FFmpeg: $_"
        Write-Warning "You may need to install this manually"
    }
} else {
    $ffmpegVersion = ffmpeg -version 2>&1 | Select-Object -First 1
    Show-Success "FFmpeg is already installed"
}

# 9. Check for Rust (via Chocolatey)
Show-Info "Checking for Rust..."
if (-not (Test-CommandExists "rustc")) {
    Write-Warning "Rust is not installed. Installing via Chocolatey..."

    # Check for Chocolatey
    if (-not (Test-CommandExists "choco")) {
        Show-Info "Chocolatey is not installed. Installing..."
        try {
            winget install Chocolatey.Chocolatey --accept-source-agreements --accept-package-agreements --silent
            Refresh-EnvironmentPath
            Show-Success "Chocolatey installed successfully"
        } catch {
            Write-Error "Failed to install Chocolatey: $_"
            Write-Warning "Skipping Rust installation"
        }
    } else {
        Show-Success "Chocolatey is already installed"
    }

    # Install Rust if Chocolatey is now available
    if (Test-CommandExists "choco") {
        Show-Info "Installing Rust via Chocolatey..."
        try {
            choco install rust -y
            Refresh-EnvironmentPath
            Show-Success "Rust installed successfully"
        } catch {
            Write-Error "Failed to install Rust: $_"
            Write-Warning "You may need to install this manually"
        }
    }
} else {
    $rustVersion = rustc --version
    Show-Success "Rust is already installed: $rustVersion"
}

# 10. Configuration Files Setup
Write-Header "Setting Up Configuration Files"

# Copy .env file
if (Test-Path ".env") {
    Show-Success "Config file (.env) already exists"
} else {
    if (Test-Path "example.env") {
        Show-Info "Copying example.env to .env..."
        Copy-Item "example.env" ".env"
        Show-Success "Created .env file"
        Write-Warning "Please edit the .env file to configure your API keys"

        # Open in default text editor
        Show-Info "Opening .env in editor..."
        notepad.exe .env
    } else {
        Write-Warning "example.env not found, skipping .env creation"
    }
}

# Copy local workspaces config
if (Test-Path ".local_workspaces.json") {
    Show-Success "Local workspaces config already exists"
} else {
    if (Test-Path "local_workspaces.example.json") {
        Show-Info "Creating local workspaces config..."
        Copy-Item "local_workspaces.example.json" ".local_workspaces.json"
        Show-Success "Created .local_workspaces.json"
    } else {
        Write-Warning "local_workspaces.example.json not found, skipping"
    }
}

# Copy demo .env.local
$demoEnvPath = "src\typescript_client_sdk\packages\demo\.env.local"
$demoEnvExample = "src\typescript_client_sdk\packages\demo\.env.example"
if (Test-Path $demoEnvPath) {
    Show-Success "Demo config already exists"
} else {
    if (Test-Path $demoEnvExample) {
        Show-Info "Creating demo config..."
        Copy-Item $demoEnvExample $demoEnvPath
        Show-Success "Created demo .env.local"
    } else {
        Write-Warning "Demo .env.example not found, skipping"
    }
}

# 11. Activate virtual environment and install Python dependencies
Write-Header "Installing Python Dependencies"

Show-Info "Activating virtual environment..."
$activateScript = Join-Path $projectRoot ".venv\Scripts\Activate.ps1"

if (Test-Path $activateScript) {
    try {
        & $activateScript
        Show-Success "Virtual environment activated"

        # Upgrade pip
        Show-Info "Upgrading pip..."
        python -m pip install --upgrade pip --quiet
        Show-Success "Pip upgraded"

        # Install tomli
        Show-Info "Installing tomli..."
        pip install tomli --quiet
        Show-Success "tomli installed"

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

Show-Info "Configuring npm for faster installs..."
npm config set audit false
npm config set fund false
npm config set fetch-retries 0
npm config set progress false
Show-Success "npm configured"

Show-Info "Installing pnpm globally..."
try {
    npm install -g pnpm@10 --no-audit --no-fund --silent
    Show-Success "pnpm installed"
} catch {
    Write-Error "Failed to install pnpm: $_"
    exit 1
}

Show-Info "Installing lerna globally..."
try {
    $env:npm_config_ignore_scripts = "true"
    npm install -g "lerna@^9" --no-audit --no-fund --silent
    Remove-Item Env:\npm_config_ignore_scripts
    Show-Success "lerna installed"
} catch {
    Write-Error "Failed to install lerna: $_"
    exit 1
}

# 13. Install TypeScript Client SDK dependencies
Write-Header "Building TypeScript Client SDK"

$sdkPath = "src\typescript_client_sdk"
if (Test-Path $sdkPath) {
    Show-Info "Installing TypeScript Client SDK dependencies..."
    try {
        pnpm install --dir $sdkPath
        Show-Success "SDK dependencies installed"

        Show-Info "Building TypeScript Client SDK..."
        pnpm --dir $sdkPath build
        Show-Success "SDK built successfully"
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
    Show-Info "Installing Python backend dependencies..."
    try {
        & cmd /c $installDepsScript
        Show-Success "Python dependencies installed"
    } catch {
        Write-Error "Failed to install Python dependencies: $_"
        exit 1
    }
} else {
    Write-Warning "install_deps.bat not found at: $installDepsScript"
}

# Final Summary
Write-Header "Setup Complete!"

Show-Success "Initial setup completed successfully!"
Write-Host ""
Show-Info "Next steps:"
Write-ColorOutput "  1. Review and update .env file with your API keys" -Color $ColorYellow
Write-ColorOutput "  2. Activate the virtual environment:" -Color $ColorCyan
Write-ColorOutput "     .venv\Scripts\Activate.ps1" -Color $ColorCyan
Write-ColorOutput "  3. Start working on the project!" -Color $ColorGreen
Write-Host ""
Write-Warning "If you installed new tools, you may need to restart your terminal or computer"
Write-Warning "for PATH changes to take full effect."
Write-Host ""

Write-Host ""
Show-Info "Press any key to exit"
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")