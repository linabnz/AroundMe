#!/bin/bash
dos2unix bin/install.sh
#!/bin/bash

# Exit immediately if a command exits with a non-zero status
set -e

# Docker image name
IMAGE_NAME="streamlit_app"

# Check if dos2unix is installed
echo "=== Checking for 'dos2unix' ==="
if ! [ -x "$(command -v dos2unix)" ]; then
  echo "Error: 'dos2unix' is not installed. Install it using 'sudo apt install dos2unix'." >&2
  exit 1
fi

# Convert all .sh scripts to Unix format
echo "=== Converting scripts to Unix format ==="
find . -type f -name "*.sh" -exec dos2unix {} +

# Check if Docker is installed
echo "=== Checking if Docker is installed ==="
if ! [ -x "$(command -v docker)" ]; then
  echo "Error: Docker is not installed." >&2
  exit 1
fi

# Build the Docker image
echo "=== Building the Docker image ==="
docker build -t ${IMAGE_NAME} .

# Verify the built Docker image
echo "=== Verifying built images ==="
docker images | grep ${IMAGE_NAME}

# Success message
echo "=== Docker image built successfully ==="
