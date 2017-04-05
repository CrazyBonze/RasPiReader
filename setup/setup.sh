#!/bin/bash

#DIST=$(gawk -F= '/^NAME/{print $2}' /etc/os-release)
SUDO=''
if [ "$EUID" -ne 0 ]; then
  echo "Needs to run with root privileges."
  SUDO='sudo'
fi

if [ -f /etc/lsb-release ]; then
  $SUDO add-apt-repository -y ppa:fkrull/deadsnakes
  $SUDO apt-get update
  $SUDO apt-get install -y python3.5 python3.5-tk python3-pip
  $SUDO apt-get autoremove
fi

if [ -f /etc/redhat-release ]; then
  echo "Not yet implemented!"
fi

if ./test.py; then
  echo ""
  echo "Successfully set up environment!"
else
  echo ""
  echo "Failed to set up environment."
fi
