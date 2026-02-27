import pandas as pd
import os
import re
import sys

FIELDS = ["Issue Number","Risk", "Likelihood", "Severity", "Mitigations", "Ownership", "Examples"]
CSV_PATH = "register/risks.csv"

def parse_issue(body):
    values = {}
    for field in FIELDS:
        pattern = rf"### {field}\n\n(.*?)\n\n"
        match = re.search(pattern, body, re.DOTALL)
        value = match.group(1).strip() if match else ""
        values[field] = value
    return values

def update_csv_row(values, issue_number):
    file_exists = os.path.exists(CSV_PATH)
    # eror if trying to update an issue that doesn't exist in the CSV
    if values["Issue Number"] and not file_exists:
        print(f"Trying to update issue #{values['Issue Number']} but CSV doesn't exist — skipping")
        sys.exit(1)
    risk_register = pd.read_csv(CSV_PATH)
    # get relevant row from issue number
    existing_row = risk_register[risk_register["Issue"] == f"#{issue_number}"]
    if existing_row.empty:
        print(f"Trying to update issue #{issue_number} but it doesn't exist in CSV — skipping")
        sys.exit(1)
    # update row with new field, skipping any "_no response_" values
    for field in FIELDS[1:]:  # skip issue number field
        if values[field] and values[field] != "_No response_":
            existing_row[field] = values[field]

    # write updated row back to CSV
    risk_register.update(existing_row)
    risk_register.to_csv(CSV_PATH, index=False)

body = os.environ.get("ISSUE_BODY", "")
issue_number = os.environ.get("ISSUE_NUMBER", "")

values = parse_issue(body)

if not values.get("Issue Number"):
    print("Could not parse issue number from issue body — skipping")
    sys.exit(1)

update_csv_row(values, issue_number)
print(f"Updated risk from issue #{issue_number} in register")