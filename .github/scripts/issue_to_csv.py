import csv
import json
import os
import sys


FIELDS = ["Risk", "Likelihood", "Severity", "Reach", "Mitigations", "Ownership", "Examples"]
CSV_PATH = "register/risks.csv"
TAG_PREFIX = "tag:"


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


def parse_labels(raw_labels):
    if not raw_labels:
        return []
    try:
        labels = json.loads(raw_labels)
    except json.JSONDecodeError:
        return []

    tags = []
    for label in labels:
        if isinstance(label, str) and label.lower().startswith(TAG_PREFIX):
            tags.append(label.split(":", 1)[1].strip())
    return sorted(dict.fromkeys(tag for tag in tags if tag))


def upsert_csv(values, issue_number, tags):
    issue_ref = f"#{issue_number}"
    fieldnames = FIELDS + ["Tags", "Issue", "Updates", "Maintainer Notes"]
    rows = []

    if os.path.exists(CSV_PATH):
        with open(CSV_PATH, newline="", encoding="utf-8") as existing_file:
            rows = list(csv.DictReader(existing_file))

    row_data = {field: values.get(field, "") for field in FIELDS}
    row_data["Tags"] = ", ".join(tags)
    row_data["Issue"] = issue_ref
    row_data["Updates"] = issue_ref
    row_data["Maintainer Notes"] = ""

    updated = False
    for row in rows:
        if row.get("Issue") == issue_ref:
            existing_updates = row.get("Updates", issue_ref) or issue_ref
            existing_notes = row.get("Maintainer Notes", "")
            row.update(row_data)
            row["Updates"] = existing_updates
            row["Maintainer Notes"] = existing_notes
            updated = True
            break

    if not updated:
        rows.append(row_data)

    with open(CSV_PATH, "w", newline="", encoding="utf-8") as output_file:
        writer = csv.DictWriter(output_file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


if __name__ == "__main__":
    body = os.environ.get("ISSUE_BODY", "")
    issue_number = os.environ.get("ISSUE_NUMBER", "")
    raw_labels = os.environ.get("ISSUE_LABELS", "")

    values = parse_issue(body)
    tags = parse_labels(raw_labels)

    if not values.get("Risk"):
        print("Could not parse risk from issue body - skipping")
        sys.exit(1)

    upsert_csv(values, issue_number, tags)
    print(f"Synced risk from issue #{issue_number} to register")
