# Agent C Prerequisites

**Important**: Please verify and install prerequisites in the order listed below, unless you already know certain prerequisites are installed. If you install WSL and/or Rancher, you **must restart your computer** after installation before proceeding.

**Questions or Issues?** Contact **Ethan Booth** via Teams or Email.

## Table of Contents
- [WSL](#wsl)
- [Git](#git)
- [Rancher](#rancher)
- [Obtaining API Keys](#obtaining-api-keys)

---

<div style="page-break-after: always;"></div>

## WSL

**Check if WSL is installed:**

Open PowerShell and run:

```powershell
wsl --version
```

If installed, you'll see version information displayed. If not installed, you should receive an error message.

**To install WSL:**

Open PowerShell as Admin (`Windows + X` → **"PowerShell (Admin)"**) and run:

```powershell
wsl --install
```


---

## Git

**Check if Git is installed:**

Open PowerShell and run:

```powershell
git --version
```

If installed, you'll see version information displayed. If not installed, you should receive an error message.

**To install Git:**

Open PowerShell as Admin (`Windows + X` → **"PowerShell (Admin)"**) and run:

```powershell
winget install Git.Git
```

**Restart your computer after installation.**

---

<div style="page-break-after: always;"></div>

## Rancher

**Check if Rancher Desktop is installed:**

Check your Applications list to verify if Rancher Desktop is installed.

**To install Rancher Desktop:**

1. Go to https://rancherdesktop.io/
2. Click download and install for Windows
3. When prompted during setup, set the container engine to **dockerd**

**Restart your computer after installation.**

---

<div style="page-break-after: always;"></div>

## Obtaining API Keys

### Anthropic API Key

1. Go to **console.anthropic.com**
2. Sign up for an account
3. Navigate to the **API keys** section
4. Generate a new key
5. Copy it immediately (you won't be able to view it again)
6. Set up billing information to use the API beyond any initial trial credits

For detailed instructions, check out **docs.anthropic.com**.

### OpenAI API Key

1. Go to **platform.openai.com** (or **openai.com/api**)
2. Sign up for an account
3. Go to the **API keys** section (usually under account settings)
4. Click "**Create new secret key**"
5. Give it a name and copy it immediately (you won't be able to see it again)
6. Set up billing to use the API beyond any free trial credits

**Important Note**: The API platform is separate from the ChatGPT subscription. Even if you have ChatGPT Plus, you still need to set up API access separately with its own billing.
