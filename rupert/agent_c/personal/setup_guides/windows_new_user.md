# Agent C Realtime Client - Windows Setup

## Prerequisites

**Check What's Already Installed:**
```
Open PowerShell as Admin (Windows + X → "PowerShell (Admin)")
```

```powershell
wsl --version
git --version
```

If both show versions, skip to Step 1. Otherwise, continue below.

**Pre-Installation Steps (IN ORDER):**

1. **Install WSL** (MUST BE FIRST - skip if already installed):
   2. Windows Subsystem for Linux
```powershell
wsl --install
```

2. **Install Git** (skip if already installed):
```powershell
winget install Git.Git
```

3. **Download Rancher Desktop**:
   - Go to https://rancherdesktop.io/
   - Click download and install for Windows
   - Choose 'dockerd' as the container engine


4. **RESTART COMPUTER** (required after WSL + Rancher) then verify:

```powershell
wsl --version
git --version
```

---

## Step 1: Download Agent C

```powershell
cd $env:USERPROFILE
git clone https://github.com/centricconsulting/agent_c_framework.git
cd agent_c
```

---

## Step 2: Navigate to Agent C Framework

```powershell
cd agent_c
```

---

## Step 3: Initialize Local Storage

```powershell
agentc up
```
1. This creates the `.agent_c` folder with:
   2. Config file, User db, Chat session index, Agents, Saved chat files
   3. Should pop up a separate text edit file
   3. This is where we'll place the API keys

---

## Step 4: Run Startup Again

```powershell
agentc up
```

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
