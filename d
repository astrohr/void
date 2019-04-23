#!/usr/bin/env bash

export SSHKEY_PUB=$(<~/.ssh/id_rsa.pub)
docker-compose -f docker/docker-compose.yml $@
