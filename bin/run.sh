#!/bin/bash
set -e

IMAGE_NAME="streamlit_app"
CONTAINER_NAME="streamlit_container"
HOST_PORT=5002
CONTAINER_PORT=5002

echo "=== Checking if the container is already running ==="
if [ "$(docker ps -q -f name=${CONTAINER_NAME})" ]; then
  echo "Stopping the existing container..."
  docker stop ${CONTAINER_NAME}
fi

echo "=== Removing any existing container with the same name ==="
if [ "$(docker ps -aq -f name=${CONTAINER_NAME})" ]; then
  docker rm ${CONTAINER_NAME}
fi

echo "=== Running the Docker container in interactive mode ==="
docker run -it --name ${CONTAINER_NAME} -p ${HOST_PORT}:${CONTAINER_PORT} ${IMAGE_NAME}

echo "=== Exiting the container ==="
