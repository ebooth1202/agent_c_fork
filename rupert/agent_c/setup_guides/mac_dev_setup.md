# Agent C Native Development Setup - Mac

## Prerequisites

**Check What's Already Installed:**
```bash
# Open Terminal (CMD + Space → type: "Terminal")
python3 --version
git --version
node --version
```

**Install Prerequisites (IN ORDER):**

1. **Install Xcode Command Line Tools:**
```bash
xcode-select --install
```

2. **Install Homebrew** (if not already installed):
```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

3. **Install Required Packages:**
```bash
brew install python@3.12 pyenv rust node ffmpeg
```

4. **Install PyCharm Community Edition** (Recommended):
```bash
brew install --cask pycharm-ce
```

---

## Step 1: Clone Agent C Repository

```bash
cd ~
git clone https://github.com/centricconsulting/agent_c_framework.git
cd agent_c_framework
```

---

## Step 2: Run Setup Script

```bash
./scripts/initial_setup.sh
```

This will:
- Create a Python virtual environment
- Install all required dependencies
- Set up the project structure

---

## Step 3: Get API Key

**Recommended: Anthropic Claude**
- Go to: https://console.anthropic.com/
- Sign up and create an API key
- Copy the key (starts with `sk-ant-`)

**Alternative: OpenAI**
- Go to: https://platform.openai.com/
- Create API key
- Prepay minimum $20 for usage credits
- **Note:** ChatGPT Plus subscription is NOT sufficient

---

## Step 4: Configure Environment

1. **Copy the example environment file:**
```bash
cp example.env .env
```

2. **Edit .env file and add your API key:**
```bash
nano .env
```

Add your key:
```
ANTHROPIC_API_KEY=sk-ant-your-key-here
```

Save and exit (CTRL+X, then Y, then Enter)

---

## Step 5: Start Agent C

**Start the API:**
```bash
scripts/start_api.sh
```

**Start the Client:**
```bash
scripts/start_client.sh
```

---

## Step 6: Open Browser

```
https://localhost:5173/chat
```

**Bookmark / Save to Favorites**

---

**Login:** `admin` / `changeme`

**Project Location:**
- Project: `~/agent_c_framework`
- Configuration: `~/.agent_c/agent_c.config`

---

## Stopping Agent C

```bash
# Find and kill the processes
Ctrl + C
```

Or close the terminal windows where you started them.
