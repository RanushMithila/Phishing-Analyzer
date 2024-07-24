#!/bin/bash

# Exit immediately if a command exits with a non-zero status
set -e

# Install Playwright's browser dependencies
playwright install-deps

# Install Playwright browsers
playwright install
