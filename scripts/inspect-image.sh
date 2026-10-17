
#!/usr/bin/env bash
set -Eeuo pipefail

IMAGE="${1:-}"

if [[ -z "$IMAGE" ]]; then
    echo "Usage: $0 <image:tag>" >&2
    exit 2
fi

if ! command -v docker >/dev/null 2>&1; then
    echo "ERROR: Docker CLI is not installed or not in PATH." >&2
    exit 2
fi

if ! docker image inspect "$IMAGE" >/dev/null 2>&1; then
    echo "ERROR: Image not found locally: $IMAGE" >&2
    exit 1
fi

echo "=== Image: $IMAGE ==="

echo
echo "=== Image metadata ==="
docker image inspect "$IMAGE" \
    --format 'ID: {{.Id}}
Created: {{.Created}}
OS/Architecture: {{.Os}}/{{.Architecture}}
User: {{if .Config.User}}{{.Config.User}}{{else}}root (default){{end}}
Working directory: {{.Config.WorkingDir}}'

echo
echo "=== Image entrypoint and command ==="
docker image inspect "$IMAGE" \
    --format 'Entrypoint: {{json .Config.Entrypoint}}
Command: {{json .Config.Cmd}}'

echo
echo "=== Exposed ports ==="
docker image inspect "$IMAGE" \
    --format '{{json .Config.ExposedPorts}}'

echo
echo "=== Image layers ==="
docker image history "$IMAGE" --no-trunc

echo
echo "Inspection completed."
