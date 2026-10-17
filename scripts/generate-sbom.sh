
#!/usr/bin/env bash
set -Eeuo pipefail

IMAGE="${1:-}"
OUTPUT="${2:-reports/sbom.cdx.json}"

if [[ -z "$IMAGE" ]]; then
    echo "Usage: $0 <image:tag> [output-file]" >&2
    exit 2
fi

if ! command -v trivy >/dev/null 2>&1; then
    echo "ERROR: Trivy is not installed." >&2
    exit 2
fi

echo "Generating SBOM for: $IMAGE"
echo "Output file: $OUTPUT"

trivy image \
    --scanners vuln \
    --format cyclonedx \
    --output "$OUTPUT" \
    "$IMAGE"

echo "SBOM generated successfully: $OUTPUT"

#!/usr/bin/env bash
set -Eeuo pipefail

IMAGE="${1:-}"
OUTPUT="${2:-reports/sbom.cdx.json}"

if [[ -z "$IMAGE" ]]; then
    echo "Usage: $0 <image:tag> [output-file]" >&2
    exit 2
fi

if ! command -v trivy >/dev/null 2>&1; then
    echo "ERROR: Trivy is not installed." >&2
    exit 2
fi

echo "Generating SBOM for: $IMAGE"
echo "Output file: $OUTPUT"

trivy image \
    --scanners vuln \
    --format cyclonedx \
    --output "$OUTPUT" \
    "$IMAGE"

echo "SBOM generated successfully: $OUTPUT"
