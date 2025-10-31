# Agent C Realtime Client - Windows Setup

## Prerequisites

**Check What's Already Installed:**

1. **Download Rancher Desktop**:
   - Go to https://rancherdesktop.io/
   - Click download and install for Windows
   - Choose 'dockerd' as the container engine
```
Open PowerShell as Admin (Windows + X → "PowerShell (Admin)")
```

```powershell
wsl --version
```

If this shows a version, skip to Step 1. Otherwise, continue below.

**Pre-Installation Steps (IN ORDER):**

2. **Install WSL** (MUST BE FIRST - skip if already installed):
   1. Windows Subsystem for Linux
```powershell
wsl --install
```

3. **RESTART COMPUTER** (required after WSL + Rancher) then verify:

```powershell
wsl --version
```

---

## Step 1: Download Agent C
```
Open PowerShell as Admin (Windows + X → "PowerShell (Admin)")
```
```powershell
cd $env:USERPROFILE
```
```powershell
git clone https://github.com/centricconsulting/agent_c_framework.git
```

---

## Step 2: Navigate to Agent C Framework

```powershell
cd agent_c_framework
```
---

## Step 3: Navigate to Agent C Framework

```powershell
.\scripts\initial_setup.ps1
```
1. This creates the `.agent_c` folder with:
   2. Config file, User db, Chat session index, Agents, Saved chat files
   3. Should pop up a separate text edit file
   3. This is where we'll place the API keys

---

## Step 4: Run Startup 

```powershell
.\agentc up
```
- This will initiate the container builds and initiate the client


---

## Step 5: Open Browser Tab
```
https://localhost:5173/chat
```
**Bookmark / Save to Favorites**

---

**Login:** `admin` / `changeme` 

**File Locations:**
- Project: `C:\Users\YourUsername\agent_c_framework`
- Configuration: `C:\Users\YourUsername\.agent_c`
