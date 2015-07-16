#!/bin/bash

set -e

cd "$1"
find . -name '*.po' -exec msgfmt --statistics --verbose {} 2>&1 \; | analyze-po-files.py
