
#!/usr/bin/env bash
set -Eeuo pipefail

IMAGE="${1:-}"
REPORT="reports/trivy-report.json"

if [[ -z "$IMAGE" ]]; then
    echo "Usage: $0 <image:tag>" >&2
    exit 2
fi

if ! command -v docker >/dev/null 2>&1; then
    echo "ERROR: Docker CLI is not installed." >&2
    exit 2
fi

if ! docker image inspect "$IMAGE" >/dev/null 2>&1; then
    echo "ERROR: Image not found locally: $IMAGE" >&2
    exit 1
fi

if [[ ! -s "$REPORT" ]]; then
    echo "ERROR: Scan report is missing or empty: $REPORT" >&2
    echo "Run security/scan-image.sh first." >&2
    exit 1
fi

if ! python3 security/evaluate-policy.py \
    --report "$REPORT" \
    --policy security/policy.yaml; then
    echo "ERROR: Image promotion blocked by security policy." >&2
    exit 1
fi

echo "Security policy passed."
echo "Image is eligible for promotion: $IMAGE"

