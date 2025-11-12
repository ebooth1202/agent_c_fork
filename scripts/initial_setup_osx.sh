#!/usr/bin/env bash
set -e
if ! command -v brew &> /dev/null; then
  /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
  echo "Complete the Homebrew installation by following the instructions above. and rerun this script"
fi

echo "Installing build dependencies"
xcode-select --install
brew install python@3.12 pyenv rust node ffmpeg

echo "Installing mkcert using Homebrew"
brew install mkcert
brew install nss
mkcert -install
chmod a+x  scripts/generate_certs.sh
./scripts/generate_certs.sh

# Check for Python and print the version
if ! command -v python &> /dev/null; then
    echo "Python is not installed or not in the PATH."
    exit 1
fi

# Check if the virtual environment already exists
if [ -d ".venv" ]; then
    echo "Virtual environment already exists. Skipping creation."
else
    echo "Creating virtual environment"
    # Create a virtual environment
    python -m venv .venv
fi

# Activate the virtual environment
echo "Activating virtual environment"
source .venv/bin/activate

echo "Upgrading pip to the latest version"
pip install --upgrade pip

echo "Installing pnpm version 9 and lerna globally"
npm install -g pnpm@9 lerna

echo "Fetching initial client dependencies with pnpm..."
cd src/typescript_client_sdk
pnpm install
cd ../..


# Install the requirements
echo "Installing deps"
chmod a+x scripts/install_deps.sh
./scripts/install_deps.sh
echo "Remember to activate the virtual environment with 'source .venv/bin/activate' before you start working."

# Exit from the script without deactivating (since it's a new shell instance)
