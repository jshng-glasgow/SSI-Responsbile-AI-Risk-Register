import pandas as pd
import os
import re
import sys

FIELDS = ["Issue Number","Risk", "Likelihood", "Severity", "Mitigations", "Ownership", "Examples"]
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
            values[field] = None if content in ("_No response_", "", "None", "No changes") else content
    return values

def update_csv_row(values, issue_number):
    file_exists = os.path.exists(CSV_PATH)
    # eror if trying to update an issue that doesn't exist in the CSV
    if values["Issue Number"] and not file_exists:
        print(f"Trying to update issue #{values['Issue Number']} but CSV doesn't exist — skipping")
        sys.exit(1)
    updated_issue = values['Issue Number'].replace('#', '')
    risk_register = pd.read_csv(CSV_PATH)
    # Convert all columns to object type to allow mixed string/NaN values
    risk_register = risk_register.astype(object)
    # get relevant row from issue number
    row_mask = risk_register["Issue"] == f"#{updated_issue}"
    if not row_mask.any():
        print(f"Trying to update issue #{updated_issue} but it doesn't exist in CSV — skipping")
        sys.exit(1)
    
    # Get the index of the row to update
    row_index = risk_register[row_mask].index[0]
    
    # update row with new field, skipping any None values
    for field in FIELDS[1:]:  # skip issue number field
        if values[field] is not None:
            risk_register.loc[row_index, field] = values[field]
    
    # Append the update issue number to the Updates column
    update_issue = f"#{issue_number}"  # The current issue number (update request)
    current_updates = risk_register.loc[row_index, 'Updates'] if 'Updates' in risk_register.columns else ''
    if pd.notna(current_updates) and current_updates:
        risk_register.loc[row_index, 'Updates'] = f"{current_updates}, {update_issue}"
    else:
        risk_register.loc[row_index, 'Updates'] = update_issue

    # write updated row back to CSV
    risk_register.to_csv(CSV_PATH, index=False)

if __name__ == "__main__":
    body = os.environ.get("ISSUE_BODY", "")
    issue_number = os.environ.get("ISSUE_NUMBER", "")

    values = parse_issue(body)

    if not values.get("Issue Number"):
        print("Could not parse issue number from issue body — skipping")
        sys.exit(1)

    update_csv_row(values, issue_number)
    print(f"Updated risk from issue {values['Issue Number']} in register")