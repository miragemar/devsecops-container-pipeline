REPORT="reports/trivy-report.json"

echo "Scanning image: $IMAGE"
echo "JSON report: $REPORT"

trivy image \
    --scanners vuln \
    --format json \
    --output "$REPORT" \
    "$IMAGE"

echo "Scan completed."
echo "Report saved to: $REPORT"
