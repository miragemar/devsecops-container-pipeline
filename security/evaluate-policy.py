
#!/usr/bin/env python3

import argparse
import json
import sys
from pathlib import Path

import yaml


DEFAULT_POLICY = Path("security/policy.yaml")


def load_policy(path):
    with path.open("r", encoding="utf-8") as file:
        policy = yaml.safe_load(file)

    if not isinstance(policy, dict):
        raise ValueError("Policy must be a YAML mapping.")

    limits = policy.get("max_vulnerabilities")
    if not isinstance(limits, dict):
        raise ValueError("Policy must define max_vulnerabilities.")

    valid_severities = {
        "CRITICAL", "HIGH", "MEDIUM", "LOW", "UNKNOWN"
    }

    for severity in valid_severities:
        value = limits.get(severity)
        if not isinstance(value, int) or isinstance(value, bool) or value < 0:
            raise ValueError(
                f"Invalid or missing limit for {severity}: {value!r}"
            )

    fail_on_unknown = policy.get("fail_on_unknown")
    if not isinstance(fail_on_unknown, bool):
        raise ValueError("fail_on_unknown must be true or false.")

    return limits, fail_on_unknown


def load_report(path):
    with path.open("r", encoding="utf-8") as file:
        report = json.load(file)

    if not isinstance(report, dict) or not isinstance(
        report.get("Results"), list
    ):
        raise ValueError("Invalid Trivy JSON report: missing Results list.")

    return report


def count_vulnerabilities(report):
    counts = {
        "CRITICAL": 0,
        "HIGH": 0,
        "MEDIUM": 0,
        "LOW": 0,
        "UNKNOWN": 0,
    }

    for result in report["Results"]:
        if not isinstance(result, dict):
            raise ValueError("Invalid entry in Trivy Results.")

        vulnerabilities = result.get("Vulnerabilities") or []
        if not isinstance(vulnerabilities, list):
            raise ValueError("Invalid Vulnerabilities field in report.")

        for vulnerability in vulnerabilities:
            if not isinstance(vulnerability, dict):
                raise ValueError("Invalid vulnerability entry.")

            severity = vulnerability.get("Severity", "UNKNOWN")
            if not isinstance(severity, str):
                raise ValueError("Invalid vulnerability severity.")

            severity = severity.upper()
            if severity not in counts:
                severity = "UNKNOWN"

            counts[severity] += 1

    return counts


def main():
    parser = argparse.ArgumentParser(
        description="Evaluate a Trivy JSON report against a security policy."
    )
    parser.add_argument(
        "--report",
        default="reports/trivy-report.json",
        help="Path to the Trivy JSON report.",
    )
    parser.add_argument(
        "--policy",
        default=str(DEFAULT_POLICY),
        help="Path to the YAML security policy.",
    )
    args = parser.parse_args()

    try:
        limits, fail_on_unknown = load_policy(Path(args.policy))
        report = load_report(Path(args.report))
        counts = count_vulnerabilities(report)
    except (OSError, json.JSONDecodeError, yaml.YAMLError, ValueError) as error:
        print(f"ERROR: Cannot evaluate policy: {error}", file=sys.stderr)
        return 2

    print("=== Vulnerability summary ===")
    for severity, count in counts.items():
        print(f"{severity:8} {count:>5} (maximum allowed: {limits[severity]})")

    violations = []

    for severity, count in counts.items():
        if count > limits[severity]:
            violations.append(
                f"{severity}: {count} found, maximum allowed is "
                f"{limits[severity]}"
            )

    if fail_on_unknown and counts["UNKNOWN"] > 0:
        message = "UNKNOWN severity vulnerabilities are not permitted."
        if message not in violations:
            violations.append(message)

    if violations:
        print("\nPOLICY FAILED")
        for violation in violations:
            print(f"- {violation}")
        return 1

    print("\nPOLICY PASSED")
    return 0


if __name__ == "__main__":
    sys.exit(main())
