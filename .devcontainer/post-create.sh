#!/usr/bin/env bash

echo "Make execution stricter - exit on failures or undefined variables ..."
set -euo pipefail

echo "Installing uv ..."
curl -LsSf https://astral.sh/uv/install.sh | sh

echo "Installing Python dependencies ..."
pip install --upgrade pip
pip install -r requirements.txt --quiet

echo "Installing latest Azure CLI from official Microsoft repository ..."
# The devcontainer azure-cli feature can ship an outdated CLI whose modules
# (e.g. monitor, rdbms) are incompatible with Python 3.12. Reinstall from the
# official Microsoft apt repository to get the latest stable build.
curl -sL https://aka.ms/InstallAzureCLIDeb | sudo bash
az version
