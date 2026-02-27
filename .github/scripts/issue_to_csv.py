import csv
import os
import re
import sys

FIELDS = ["Risk", "Likelihood", "Severity", "Mitigations", "Ownership", "Examples"]
CSV_PATH = "register/risks.csv"

def parse_issue(body):
    values = {}
    sections = body.split("### ")
    for section in sections:
        if not section.strip():
            continue
        lines = section.strip().split("\n", 1)
        field = lines[0].strip()
        content = lines[1].strip() if len(lines) > 1 else ""
        if field in FIELDS:
            values[field] = "" if content in ("_No response_", "") else content
    return values

def append_to_csv(values, issue_number):
    file_exists = os.path.exists(CSV_PATH)
    with open(CSV_PATH, "a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDS + ["Issue"])
        if not file_exists:
            writer.writeheader()
        values["Issue"] = f"#{issue_number}"
        writer.writerow(values)

body = os.environ.get("ISSUE_BODY", "")
issue_number = os.environ.get("ISSUE_NUMBER", "")

values = parse_issue(body)

if not values.get("Risk"):
    print("Could not parse risk from issue body — skipping")
    sys.exit(1)

append_to_csv(values, issue_number)
print(f"Appended risk from issue #{issue_number} to register")