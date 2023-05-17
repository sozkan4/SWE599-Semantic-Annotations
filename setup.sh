# This script is used to initialize the environment
#!/bin/bash

git clean -fd -x

cd app_server
DOCKER_COMPOSE_FILE="./docker-compose.yml"
CONTAINER_UID=$(id -u) CONTAINER_GID=$(id -g) docker-compose -f ${DOCKER_COMPOSE_FILE} stop
CONTAINER_UID=$(id -u) CONTAINER_GID=$(id -g) docker-compose -f ${DOCKER_COMPOSE_FILE} rm --force
CONTAINER_UID=$(id -u) CONTAINER_GID=$(id -g) docker-compose -f ${DOCKER_COMPOSE_FILE} build
CONTAINER_UID=$(id -u) CONTAINER_GID=$(id -g) docker-compose -f ${DOCKER_COMPOSE_FILE} up -d --remove-orphans


cd ../annotation_server
DOCKER_COMPOSE_FILE="./docker-compose.yml"
CONTAINER_UID=$(id -u) CONTAINER_GID=$(id -g) docker-compose -f ${DOCKER_COMPOSE_FILE} stop
CONTAINER_UID=$(id -u) CONTAINER_GID=$(id -g) docker-compose -f ${DOCKER_COMPOSE_FILE} rm --force
CONTAINER_UID=$(id -u) CONTAINER_GID=$(id -g) docker-compose -f ${DOCKER_COMPOSE_FILE} build
CONTAINER_UID=$(id -u) CONTAINER_GID=$(id -g) docker-compose -f ${DOCKER_COMPOSE_FILE} up -d --remove-orphans

cd ..