import os
import sys
from unittest.mock import patch

import pandas as pd

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".github", "scripts"))

from issue_to_csv import combine_tags, parse_issue, split_tags, upsert_csv


class TestIssueToCSV:
    def test_parse_issue_complete(self):
        body = """### Risk
Test risk description

### Likelihood
High

### Severity
Medium

### Reach
Low

### Mitigations
Some mitigations

### Ownership
Test owner

### Examples
Test examples

### Tags
Economic, Environmental

### Other Tags
Local Practice
"""
        values = parse_issue(body)
        assert values["Risk"] == "Test risk description"
        assert values["Likelihood"] == "High"
        assert values["Severity"] == "Medium"
        assert values["Reach"] == "Low"
        assert values["Mitigations"] == "Some mitigations"
        assert values["Ownership"] == "Test owner"
        assert values["Examples"] == "Test examples"
        assert values["Tags"] == "Economic, Environmental, Local Practice"

    def test_parse_issue_no_response(self):
        body = """### Risk
Test risk

### Likelihood
_No response_

### Severity
Medium

### Reach
Unknown

### Mitigations


### Ownership
_No response_

### Examples
Examples

### Tags
_No response_

### Other Tags
"""
        values = parse_issue(body)
        assert values["Risk"] == "Test risk"
        assert values["Likelihood"] == ""
        assert values["Severity"] == "Medium"
        assert values["Reach"] == "Unknown"
        assert values["Mitigations"] == ""
        assert values["Ownership"] == ""
        assert values["Examples"] == "Examples"
        assert values["Tags"] == ""

    def test_split_tags_supports_commas_and_newlines(self):
        assert split_tags("Economic, Environmental\nGovernance") == ["Economic", "Environmental", "Governance"]

    def test_combine_tags_deduplicates(self):
        assert combine_tags("Economic, Environmental", "Environmental, Local Practice") == "Economic, Environmental, Local Practice"

    def test_upsert_csv_new_file(self, tmp_path):
        test_csv = tmp_path / "risks.csv"

        with patch("issue_to_csv.CSV_PATH", str(test_csv)):
            values = {
                "Risk": "Test risk",
                "Likelihood": "High",
                "Severity": "Medium",
                "Reach": "Low",
                "Mitigations": "Mitigations",
                "Ownership": "Owner",
                "Examples": "Examples",
                "Tags": "Environmental, Training and Development",
            }
            upsert_csv(values, "123")

            df = pd.read_csv(str(test_csv))
            assert len(df) == 1
            assert df.iloc[0]["Risk"] == "Test risk"
            assert df.iloc[0]["Issue"] == "#123"
            assert df.iloc[0]["Updates"] == "#123"
            assert df.iloc[0]["Reach"] == "Low"
            assert df.iloc[0]["Tags"] == "Environmental, Training and Development"
            assert pd.isna(df.iloc[0]["Maintainer Notes"]) or df.iloc[0]["Maintainer Notes"] == ""

    def test_upsert_csv_existing_issue_updates_tags_without_duplicates(self, tmp_path):
        test_csv = tmp_path / "risks.csv"
        existing_df = pd.DataFrame(
            {
                "Risk": ["Existing risk"],
                "Likelihood": ["Low"],
                "Severity": ["High"],
                "Reach": ["Medium"],
                "Mitigations": ["Existing mitigations"],
                "Ownership": ["Existing owner"],
                "Examples": ["Existing examples"],
                "Tags": ["Environmental"],
                "Issue": ["#124"],
                "Updates": ["#124"],
                "Maintainer Notes": ["Keep this note"],
            }
        )
        existing_df.to_csv(str(test_csv), index=False)

        with patch("issue_to_csv.CSV_PATH", str(test_csv)):
            values = {
                "Risk": "Existing risk revised",
                "Likelihood": "High",
                "Severity": "Medium",
                "Reach": "Very High",
                "Mitigations": "New mitigations",
                "Ownership": "New owner",
                "Examples": "New examples",
                "Tags": "Research Integrity",
            }
            upsert_csv(values, "124")

            df = pd.read_csv(str(test_csv))
            assert len(df) == 1
            assert df.iloc[0]["Risk"] == "Existing risk revised"
            assert df.iloc[0]["Issue"] == "#124"
            assert df.iloc[0]["Updates"] == "#124"
            assert df.iloc[0]["Reach"] == "Very High"
            assert df.iloc[0]["Tags"] == "Research Integrity"
            assert df.iloc[0]["Maintainer Notes"] == "Keep this note"
