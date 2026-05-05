#!/usr/bin/env bash
set -euo pipefail

sudo apt-get update -y
sudo apt-get install -y qemu-guest-agent python3 sudo
sudo systemctl enable qemu-guest-agent
sudo systemctl restart qemu-guest-agent
