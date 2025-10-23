# Agent C Realtime Client - Mac Setup

## Prerequisites

**Check What's Already Installed:**
```
Open Terminal (CMD+ Space Bar → type in: "Terminal"
```

```
git --version
```

If git shows a version, skip to Step 1. Otherwise, continue below.

**Pre-Installation Steps (IN ORDER):**

1. **Install Git** (skip if already installed):
```
xcode-select --install 
```
-  If you want to install using Homebrew:
```
- /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
- brew install git
```

2. **Download Docker Desktop**:
   - Go to https://www.docker.com/products/docker-desktop/
   - Click download and install for Mac
   - Choose correct version:
   ```
   - Mac with Apple chip (M1, M2, M3, etc.)
   - Mac with Intel Chip
   ```
   - Choose 'dockerd' as the container engine


---

## Step 1: Download Agent C

```terminal
cd $env:USERPROFILE
git clone https://github.com/centricconsulting/agent_c_framework.git
```

---

## Step 2: Navigate to Agent C Framework

```terminal
cd agent_c
```

---

## Step 3: Initialize Local Storage

```terminal
agentc up
```
1. This creates the `.agent_c` folder with:
   2. Config file, User db, Chat session index, Agents, Saved chat files
   3. Should pop up a separate text edit file
   3. This is where we'll place the API keys

---

## Step 4: Run Startup Again

```terminal
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
- Project: `Users\YourUsername\agent_c_framework`
- Configuration: `Users\YourUsername\.agent_c`
