#!/usr/bin/env bash
set -euo pipefail

sudo cloud-init clean || true
sudo truncate -s 0 /etc/machine-id || true
