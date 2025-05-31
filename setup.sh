#!/bin/bash

set -e

# 1. Install system dependencies
sudo apt-get update
sudo apt-get install -y git python3 python3-pip python3-venv curl

# 2. Install uv (universal virtualenv and pip replacement)
if ! command -v uv &> /dev/null; then
    echo "Installing uv..."
    pip3 install uv
fi

# 3. Clone the repository
# (Step removed: assume script is run inside the project directory)

# 4. Create and activate the virtual environment
uv venv
source .venv/bin/activate

# 5. Install Python dependencies
uv pip install .

# 6. Prompt for .env setup
if [ ! -f .env ]; then
    echo "OPENAI_API_KEY=\"your_openai_api_key_here\"" > .env
    echo "A .env file has been created. Please edit it to add your OpenAI API key."
else
    echo ".env file already exists. Please ensure it contains your OpenAI API key."
fi

echo "Setup complete! To run the example:"
echo "source .venv/bin/activate"
