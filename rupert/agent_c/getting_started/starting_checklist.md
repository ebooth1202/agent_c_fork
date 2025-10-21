# Agent C Framework Setup Checklist

## Obtaining API Keys

### Anthropic API Key

A new user should go to **console.anthropic.com** to get their first Anthropic API key.

The process is:

1. Sign up for an account at **console.anthropic.com**
2. Once logged in, navigate to the **API keys** section
3. Generate a new key
4. Copy it immediately (you won't be able to view it again)
5. Set up billing information to use the API beyond any initial trial credits

For detailed instructions and getting started guides, check out the documentation at **docs.anthropic.com**.

### OpenAI API Key

For OpenAI, a new user goes to **platform.openai.com** (or **openai.com/api**).

The process is similar:

1. Sign up for an account at **platform.openai.com**
2. Once logged in, go to the **API keys** section (usually under your account settings)
3. Click "**Create new secret key**"
4. Give it a name and copy it immediately - you won't be able to see it again
5. Set up billing to use the API beyond any free trial credits

:::important
⚡ **Important Note**: The API platform is separate from the ChatGPT subscription, so even if someone has ChatGPT Plus, they still need to set up API access separately with its own billing.
:::

## Pre-requisites
- [ ] Ensure Docker/Rancher is installed and running on your system
- [ ] Verify you have your API keys ready

## Installation Check
- [ ] Determine if Agent C Framework is already installed
  - If installed: Identify location of the Agent C Framework directory
  - If not installed: Decide on installation location

## Installation/Update
- [ ] **If not installed:** Git clone the repository
  ```bash
  git clone [repository_url] [installation_path]
  ```
- [ ] **If already installed:** Navigate to the Agent C Framework directory and update
  ```bash
  cd [path_to_agent_c_framework]
  git pull
  ```

## Initial Setup
- [ ] Start Agent C services
  ```bash
  agentc up
  ```

## Configuration
- [ ] Update config file with your API keys
  - Location: [config_file_path]
  - Required keys: [list_of_required_keys]

## Database Setup
- [ ] Copy database files from build_support directory
  ```bash
  cp [build_support_directory]/[db_files] [destination]
  ```

## Final Startup
- [ ] Start Agent C services again to apply changes
  ```bash
  agentc up
  ```

## Verification
- [ ] Verify all services are running correctly
- [ ] Test basic functionality