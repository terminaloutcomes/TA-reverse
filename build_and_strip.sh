#!/bin/bash

set -e

if [ -z "$1" ]; then
    echo "Usage: $0 <version>"
    exit 1
else
    VERSION=$1
fi

ucc-gen build --ta-version "$VERSION"
rm -rf output/TA-reverse/appserver
rm -rf output/TA-reverse/default/data/ui
rm output/TA-reverse/default/restmap.conf
rm output/TA-reverse/default/server.conf
rm output/TA-reverse/default/web.conf
ucc-gen package --path output/*