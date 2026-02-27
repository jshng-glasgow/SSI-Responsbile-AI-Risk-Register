import csv
import os
import re
import sys
from update_csv import parse_issue

FIELDS = ["Risk", "Likelihood", "Severity", "Mitigations", "Ownership", "Examples"]
CSV_PATH = "register/risks.csv"

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