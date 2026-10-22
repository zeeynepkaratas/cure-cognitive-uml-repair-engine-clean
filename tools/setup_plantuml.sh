#!/bin/sh
set -eu
version=1.2026.6
expected=89948f14c93756c7a3fb7b69078ff37e8489fd79dd430c582b931e2f65358690
target="${1:-/opt/plantuml/plantuml.jar}"
mkdir -p "$(dirname "$target")"
curl --fail --location --retry 3 "https://github.com/plantuml/plantuml/releases/download/v${version}/plantuml-${version}.jar" -o "$target"
printf '%s  %s\n' "$expected" "$target" | sha256sum --check --strict
java -jar "$target" -version
