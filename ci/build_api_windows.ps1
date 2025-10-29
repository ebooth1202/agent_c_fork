# Agent C API - Windows Build Script for Monorepo
# =================================================
# Run from repository root: .\ci\build_api_windows.ps1

param(
    [switch]$Clean,
    [switch]$Verbose,
    [switch]$SkipValidation
)

$ErrorActionPreference = "Stop"

Write-Host "==================================" -ForegroundColor Cyan
Write-Host "Agent C API - Nuitka Build" -ForegroundColor Cyan
Write-Host "==================================" -ForegroundColor Cyan
Write-Host ""

# Ensure we're in repo root
$REPO_ROOT = Split-Path -Parent $PSScriptRoot
if (-not (Test-Path "$REPO_ROOT\src\agent_c_api")) {
    Write-Host "ERROR: Must run from repository root" -ForegroundColor Red
    Write-Host "Current location: $PWD" -ForegroundColor Red
    Write-Host "Expected: Repository root with src/agent_c_api/" -ForegroundColor Red
    exit 1
}

Set-Location $REPO_ROOT

# ==============================================
# VIRTUAL ENVIRONMENT ACTIVATION
# ==============================================

$VENV_PATH = Join-Path $REPO_ROOT ".venv"
if (Test-Path $VENV_PATH) {
    Write-Host "Activating virtual environment..." -ForegroundColor Cyan
    $VENV_ACTIVATE = Join-Path $VENV_PATH "Scripts\Activate.ps1"
    if (Test-Path $VENV_ACTIVATE) {
        & $VENV_ACTIVATE
        Write-Host "Virtual environment activated: .venv" -ForegroundColor Green
        Write-Host ""
    } else {
        Write-Host "WARNING: .venv exists but activation script not found" -ForegroundColor Yellow
        Write-Host "         Continuing with system Python" -ForegroundColor Yellow
        Write-Host ""
    }
} else {
    Write-Host "No .venv found, using system Python" -ForegroundColor Yellow
    Write-Host ""
}

# ==============================================
# PRE-FLIGHT VALIDATION
# ==============================================

if (-not $SkipValidation) {
    Write-Host "Running pre-flight checks..." -ForegroundColor Yellow
    Write-Host ""
    
    $validationFailed = $false
    
    # 1. Check Python version
    Write-Host "[1/7] Checking Python version..." -NoNewline
    $pythonCmd = Get-Command python -ErrorAction SilentlyContinue
    if ($pythonCmd) {
        $pythonVersionOutput = & $pythonCmd.Source --version 2>&1
        if ($pythonVersionOutput -match "Python (\d+)\.(\d+)") {
            $major = [int]$matches[1]
            $minor = [int]$matches[2]
            if ($major -ge 3 -and $minor -ge 12) {
                Write-Host " OK (Python $major.$minor)" -ForegroundColor Green
            } else {
                Write-Host " FAIL (Need 3.12+, found $major.$minor)" -ForegroundColor Red
                $validationFailed = $true
            }
        }
    } else {
        Write-Host " FAIL (not in PATH)" -ForegroundColor Red
        $validationFailed = $true
    }
    
    # 2. Check Nuitka
    Write-Host "[2/7] Checking Nuitka..." -NoNewline
    $nuitkaCheck = Get-Command nuitka  -ErrorAction SilentlyContinue
    if ($nuitkaCheck ) {
        Write-Host " OK" -ForegroundColor Green
    } else {
        Write-Host " FAIL" -ForegroundColor Red
        Write-Host "      Install: pip install nuitka ordered-set" -ForegroundColor Yellow
        $validationFailed = $true
    }
    
    # 3. Check MSVC
    Write-Host "[3/7] Checking MSVC (cl.exe)..." -NoNewline
    $clCmd = Get-Command cl.exe -ErrorAction SilentlyContinue
    if ($clCmd) {
        Write-Host " OK" -ForegroundColor Green
        Write-Host "      Path: $($clCmd.Source)" -ForegroundColor DarkGray
    } else {
        Write-Host " FAIL (not in PATH)" -ForegroundColor Red
        Write-Host "" 
        Write-Host "      Run from 'Developer PowerShell for VS 2022', OR:" -ForegroundColor Yellow
        Write-Host "      & 'C:\Program Files\Microsoft Visual Studio\2022\BuildTools\Common7\Tools\Launch-VsDevShell.ps1'" -ForegroundColor Cyan
        Write-Host ""
        $validationFailed = $true
    }
    


    # 6. Check/create cache directory
    Write-Host "[6/7] Setting up cache..." -NoNewline
    $CACHE_DIR = Join-Path $REPO_ROOT "build_cache\nuitka"
    if (-not (Test-Path $CACHE_DIR)) {
        New-Item -ItemType Directory -Force -Path $CACHE_DIR | Out-Null
        Write-Host " Created" -ForegroundColor Yellow
    } else {
        $cacheSize = (Get-ChildItem $CACHE_DIR -Recurse -File -ErrorAction SilentlyContinue | Measure-Object -Property Length -Sum).Sum / 1MB
        if ($cacheSize -gt 0) {
            Write-Host " OK ($([math]::Round($cacheSize, 2)) MB)" -ForegroundColor Green
        } else {
            Write-Host " Empty (first build)" -ForegroundColor Yellow
        }
    }
    
    # 7. Check disk space
    Write-Host "[7/7] Checking disk space..." -NoNewline
    $drive = (Get-Item $REPO_ROOT).PSDrive
    $freeGB = [math]::Round($drive.Free / 1GB, 2)
    if ($freeGB -gt 10) {
        Write-Host " OK ($freeGB GB free)" -ForegroundColor Green
    } else {
        Write-Host " WARNING (Only $freeGB GB free)" -ForegroundColor Yellow
    }
    
    Write-Host ""
    
    if ($validationFailed) {
        Write-Host "==================================" -ForegroundColor Red
        Write-Host "PRE-FLIGHT CHECK FAILED" -ForegroundColor Red
        Write-Host "==================================" -ForegroundColor Red
        exit 1
    }
    
    Write-Host "Pre-flight checks passed!" -ForegroundColor Green
    Write-Host ""
}

# ==============================================
# BUILD CONFIGURATION
# ==============================================

$OUTPUT_DIR = Join-Path $REPO_ROOT "dist"
$OUTPUT_NAME = "agent-c-api"
$MAIN_SCRIPT = "src\agent_c_api\src\agent_c_api\main.py"
$CACHE_DIR = Join-Path $REPO_ROOT "build_cache\nuitka"

# Ensure cache directory exists
New-Item -ItemType Directory -Force -Path $CACHE_DIR | Out-Null

# Set cache location via environment variable (proper Nuitka way)
$env:NUITKA_CACHE_DIR = $CACHE_DIR
Write-Host "Cache location: $env:NUITKA_CACHE_DIR" -ForegroundColor DarkGray
Write-Host ""

# Clean if requested
if ($Clean) {
    Write-Host "Cleaning previous build..." -ForegroundColor Yellow
    if (Test-Path $OUTPUT_DIR) {
        Remove-Item -Recurse -Force $OUTPUT_DIR
    }
    Write-Host "Clean complete." -ForegroundColor Green
    Write-Host ""
}

# ==============================================
# NUITKA ARGUMENTS
# ==============================================

$NUITKA_ARGS = @(
    # Core options
    "--jobs=10"

    # Output
    "--output-dir=$OUTPUT_DIR"


    # Main script
    $MAIN_SCRIPT
)


Write-Host "Link-time optimization enabled" -ForegroundColor Yellow
$NUITKA_ARGS += "--lto=yes"

# Verbose output
if ($Verbose) {
    $NUITKA_ARGS += "--show-memory"
}

# ==============================================
# BUILD
# ==============================================

Write-Host "Build Configuration:" -ForegroundColor Cyan
Write-Host "  Main Script:  $MAIN_SCRIPT" -ForegroundColor White
Write-Host "  Output:       $OUTPUT_DIR\$OUTPUT_NAME.dist\" -ForegroundColor White
Write-Host "  Cache:        $CACHE_DIR" -ForegroundColor White
Write-Host ""



$startTime = Get-Date

try {
    & python -m nuitka @NUITKA_ARGS
    
    if ($LASTEXITCODE -ne 0) {
        throw "Nuitka compilation failed with exit code $LASTEXITCODE"
    }
    
    $endTime = Get-Date
    $duration = $endTime - $startTime
    
    Write-Host ""
    Write-Host "==================================" -ForegroundColor Green
    Write-Host "✅ Build Successful!" -ForegroundColor Green
    Write-Host "==================================" -ForegroundColor Green
    Write-Host "Duration: $($duration.ToString('hh\:mm\:ss'))" -ForegroundColor White
    Write-Host ""
    
    # Show output info
    $distPath = Join-Path $OUTPUT_DIR "$OUTPUT_NAME.dist"
    if (Test-Path $distPath) {
        $sizeInfo = Get-ChildItem $distPath -Recurse -File | Measure-Object -Property Length -Sum
        $sizeMB = [math]::Round($sizeInfo.Sum / 1MB, 2)
        $fileCount = $sizeInfo.Count
        
        Write-Host "Output:" -ForegroundColor Cyan
        Write-Host "  Location: $distPath" -ForegroundColor White
        Write-Host "  Size:     $sizeMB MB" -ForegroundColor White
        Write-Host "  Files:    $fileCount" -ForegroundColor White
        Write-Host ""
    }
    
    # Show cache growth
    $cacheInfo = Get-ChildItem $CACHE_DIR -Recurse -File -ErrorAction SilentlyContinue | Measure-Object -Property Length -Sum
    $cacheMB = [math]::Round($cacheInfo.Sum / 1MB, 2)
    Write-Host "Cache: $cacheMB MB" -ForegroundColor DarkGray
    Write-Host ""
    
    Write-Host "Next Steps:" -ForegroundColor Cyan
    Write-Host "1. Test: cd $distPath && .\$OUTPUT_NAME.exe" -ForegroundColor White
    Write-Host "2. Next build will reuse cache (much faster!)" -ForegroundColor White
    Write-Host ""
    
} catch {
    Write-Host ""
    Write-Host "==================================" -ForegroundColor Red
    Write-Host "❌ Build Failed" -ForegroundColor Red
    Write-Host "==================================" -ForegroundColor Red
    Write-Host $_.Exception.Message -ForegroundColor Red
    Write-Host ""
    Write-Host "Cache preserved for next attempt: $CACHE_DIR" -ForegroundColor Yellow
    exit 1
}
