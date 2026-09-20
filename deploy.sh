#!/bin/sh
# Copies only what must be published into dist/ (no sources, tools or data).
set -e
cd "$(dirname "$0")"
python3 build.py
rm -rf dist && mkdir dist
rsync -a --exclude 'tools' --exclude 'data' --exclude '_scenes' --exclude 'dist' --exclude '__pycache__' --exclude '*.py' --exclude 'deploy.sh' --exclude 'README.md' --exclude 'IMAGES.md' ./ dist/
echo "dist/ ready: $(find dist -type f | wc -l) files, $(du -sh dist | cut -f1)"
