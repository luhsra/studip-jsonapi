#!/usr/bin/env bash

read -p "Enter release version (semantic, e.g. 1.2.3): " VERSION

set +x

git tag --sign -a "v${VERSION}" -m "Released version ${VERSION}"
git tag -l
git push origin "v${VERSION}"
