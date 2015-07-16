#!/bin/bash

set -e
cd "$1"

find . -name '*.pot' -print0 | while read -d '' -r f; do
    pushd "$(dirname "$f")"
    find . -name '*.po' -exec msgmerge -U {} "$(basename "$f")" \;
    popd
done
