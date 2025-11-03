#!/usr/bin/env bash
set -e
mkcert -cert-file agent_c_config/certs/dev_cert.pem -key-file agent_c_config/certs/dev_key.pem localhost agentc.local host.docker.internal `hostname`