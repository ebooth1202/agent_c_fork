# Agent C API - Windows Build Script for Monorepo
# =================================================
# Run from repository root: .\ci\build_api_windows.ps1

param(
    [switch]$Clean,
    [switch]$Verbose,
    [switch]$OptimizeSize,
    [switch]$SkipValidation,
    [switch]$Full  # Include all ML libraries (larger build)
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
    try {
        $pythonVersion = python --version 2>&1
        if ($pythonVersion -match "Python (\d+)\.(\d+)") {
            $major = [int]$matches[1]
            $minor = [int]$matches[2]
            if ($major -ge 3 -and $minor -ge 12) {
                Write-Host " OK ($pythonVersion)" -ForegroundColor Green
            } else {
                Write-Host " FAIL (Need Python 3.12+, found $pythonVersion)" -ForegroundColor Red
                $validationFailed = $true
            }
        }
    } catch {
        Write-Host " FAIL (Python not found)" -ForegroundColor Red
        $validationFailed = $true
    }
    
    # 2. Check Nuitka
    Write-Host "[2/7] Checking Nuitka..." -NoNewline
    try {
        $nuitkaVersion = python -m nuitka --version 2>&1
        if ($nuitkaVersion -match "\d+\.\d+") {
            Write-Host " OK (v$($nuitkaVersion.Trim()))" -ForegroundColor Green
        } else {
            Write-Host " FAIL" -ForegroundColor Red
            Write-Host "      Install: pip install nuitka ordered-set" -ForegroundColor Yellow
            $validationFailed = $true
        }
    } catch {
        Write-Host " FAIL" -ForegroundColor Red
        $validationFailed = $true
    }
    
    # 3. Check MSVC
    Write-Host "[3/7] Checking MSVC..." -NoNewline
    try {
        $clTest = cl.exe /? 2>&1
        if ($clTest -match "Microsoft") {
            Write-Host " OK" -ForegroundColor Green
        } else {
            throw "cl.exe not working"
        }
    } catch {
        Write-Host " FAIL" -ForegroundColor Red
        Write-Host "" 
        Write-Host "      Run from 'Developer PowerShell for VS 2022', OR:" -ForegroundColor Yellow
        Write-Host "      & 'C:\Program Files\Microsoft Visual Studio\2022\BuildTools\Common7\Tools\Launch-VsDevShell.ps1'" -ForegroundColor Cyan
        Write-Host ""
        $validationFailed = $true
    }
    
    # 4. Check API source
    Write-Host "[4/7] Checking API source..." -NoNewline
    if (Test-Path "src\agent_c_api\src\agent_c_api\main.py") {
        Write-Host " OK" -ForegroundColor Green
    } else {
        Write-Host " FAIL (main.py not found)" -ForegroundColor Red
        $validationFailed = $true
    }
    
    # 5. Check agent_c packages
    Write-Host "[5/7] Checking agent_c packages..." -NoNewline
    try {
        $coreOK = python -c "import agent_c; print('OK')" 2>&1
        $toolsOK = python -c "import agent_c_tools; print('OK')" 2>&1
        if ($coreOK -match "OK" -and $toolsOK -match "OK") {
            Write-Host " OK" -ForegroundColor Green
        } else {
            Write-Host " FAIL" -ForegroundColor Red
            Write-Host "      Install packages from monorepo first" -ForegroundColor Yellow
            $validationFailed = $true
        }
    } catch {
        Write-Host " FAIL" -ForegroundColor Red
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
    "--standalone"
    "--assume-yes-for-downloads"
    
    # Output
    "--output-dir=$OUTPUT_DIR"
    "--output-filename=$OUTPUT_NAME.exe"
    
    # Explicit cache location (avoid nested Nuitka\Nuitka issue)
    "--cache-dir=$CACHE_DIR"
    
    # Include packages
    "--include-package=agent_c_api"
    "--follow-import-to=agent_c"
    "--follow-import-to=agent_c_tools"
    
    # ============================================
    # ALWAYS EXCLUDE (tests, dev tools)
    # ============================================
    "--nofollow-import-to=agent_c_api.tests"
    "--nofollow-import-to=agent_c.tests"
    "--nofollow-import-to=agent_c_tools.tests"
    "--nofollow-import-to=pytest"
    "--nofollow-import-to=_pytest"
    "--nofollow-import-to=unittest"
    "--nofollow-import-to=test"
    
    # ============================================
    # PLUGINS
    # ============================================
    "--enable-plugin=anti-bloat"
    "--enable-plugin=no-qt"
    
    # ============================================
    # MODULE PARAMETERS
    # ============================================
    "--module-parameter=torch-disable-jit=yes"
    
    # Progress
    "--show-progress"
    
    # Main script
    $MAIN_SCRIPT
)

# ============================================
# SIZE OPTIMIZATION: Exclude heavy ML libs
# ============================================

if (-not $Full) {
    Write-Host "Building LITE version (excluding heavy ML libraries)" -ForegroundColor Yellow
    Write-Host "  - Transformers, Torch, TensorFlow excluded" -ForegroundColor DarkGray
    Write-Host "  - Tools using these will fail gracefully" -ForegroundColor DarkGray
    Write-Host "  - Use -Full flag for complete build" -ForegroundColor DarkGray
    Write-Host ""
    
    $NUITKA_ARGS += @(
        "--nofollow-import-to=transformers"
        "--nofollow-import-to=torch"
        "--nofollow-import-to=tensorflow"
        "--nofollow-import-to=tensorboard"
        # Add more as needed:
        # "--nofollow-import-to=selenium"
        # "--nofollow-import-to=playwright"
    )
} else {
    Write-Host "Building FULL version (including all dependencies)" -ForegroundColor Yellow
    Write-Host "  - This will take longer and produce a larger executable" -ForegroundColor DarkGray
    Write-Host ""
}

# LTO optimization
if ($OptimizeSize) {
    Write-Host "Link-time optimization enabled" -ForegroundColor Yellow
    $NUITKA_ARGS += "--lto=yes"
}

# Verbose output
if ($Verbose) {
    $NUITKA_ARGS += "--show-memory"
    $NUITKA_ARGS += "--show-modules"
}

# ==============================================
# BUILD
# ==============================================

Write-Host "Build Configuration:" -ForegroundColor Cyan
Write-Host "  Main Script:  $MAIN_SCRIPT" -ForegroundColor White
Write-Host "  Output:       $OUTPUT_DIR\$OUTPUT_NAME.dist\" -ForegroundColor White
Write-Host "  Cache:        $CACHE_DIR" -ForegroundColor White
Write-Host "  Build Type:   $(if ($Full) { 'FULL' } else { 'LITE' })" -ForegroundColor White
Write-Host "  Optimize:     $OptimizeSize" -ForegroundColor White
Write-Host ""

# Estimate build time
$cacheExists = (Get-ChildItem $CACHE_DIR -Recurse -File -ErrorAction SilentlyContinue).Count -gt 100
if ($cacheExists) {
    Write-Host "Estimated build time: 5-15 minutes (cache warm)" -ForegroundColor Green
} else {
    Write-Host "Estimated build time: 30-60 minutes (first build)" -ForegroundColor Yellow
    Write-Host "Subsequent builds will be MUCH faster!" -ForegroundColor Yellow
}
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
