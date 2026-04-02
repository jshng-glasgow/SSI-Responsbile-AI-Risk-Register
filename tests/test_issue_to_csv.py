import pytest
import pandas as pd
import os
import sys
from unittest.mock import patch, MagicMock

# Add the scripts directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '.github', 'scripts'))

from issue_to_csv import parse_issue, append_to_csv, FIELDS, CSV_PATH

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
"""
        values = parse_issue(body)
        assert values["Risk"] == "Test risk description"
        assert values["Likelihood"] == "High"
        assert values["Severity"] == "Medium"
        assert values["Reach"] == "Low"
        assert values["Mitigations"] == "Some mitigations"
        assert values["Ownership"] == "Test owner"
        assert values["Examples"] == "Test examples"

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
"""
        values = parse_issue(body)
        assert values["Risk"] == "Test risk"
        assert values["Likelihood"] == ""
        assert values["Severity"] == "Medium"
        assert values["Reach"] == "Unknown"
        assert values["Mitigations"] == ""
        assert values["Ownership"] == ""
        assert values["Examples"] == "Examples"

    def test_append_to_csv_new_file(self, tmp_path):
        # Mock CSV_PATH to tmp_path
        original_csv_path = CSV_PATH
        test_csv = tmp_path / "risks.csv"
        
        # Patch the CSV_PATH in the module
        with patch('issue_to_csv.CSV_PATH', str(test_csv)):
            values = {
                "Risk": "Test risk",
                "Likelihood": "High",
                "Severity": "Medium",
                "Reach": "Low",
                "Mitigations": "Mitigations",
                "Ownership": "Owner",
                "Examples": "Examples"
            }
            append_to_csv(values, "123")
            
            # Check the file was created and has correct content
            df = pd.read_csv(str(test_csv))
            assert len(df) == 1
            assert df.iloc[0]["Risk"] == "Test risk"
            assert df.iloc[0]["Issue"] == "#123"
            assert df.iloc[0]["Updates"] == "#123"
            assert df.iloc[0]["Reach"] == "Low"
            assert pd.isna(df.iloc[0]["Maintainer Notes"]) or df.iloc[0]["Maintainer Notes"] == ""

    def test_append_to_csv_existing_file(self, tmp_path):
        test_csv = tmp_path / "risks.csv"
        # Create existing CSV
        existing_df = pd.DataFrame({
            "Risk": ["Existing risk"],
            "Likelihood": ["Low"],
            "Severity": ["High"],
            "Reach": ["Medium"],
            "Mitigations": ["Existing mitigations"],
            "Ownership": ["Existing owner"],
            "Examples": ["Existing examples"],
            "Issue": ["#1"],
            "Updates": ["#1"],
            "Maintainer Notes": [""]
        })
        existing_df.to_csv(str(test_csv), index=False)
        
        with patch('issue_to_csv.CSV_PATH', str(test_csv)):
            values = {
                "Risk": "New risk",
                "Likelihood": "High",
                "Severity": "Medium",
                "Reach": "Very High",
                "Mitigations": "New mitigations",
                "Ownership": "New owner",
                "Examples": "New examples"
            }
            append_to_csv(values, "124")
            
            df = pd.read_csv(str(test_csv))
            assert len(df) == 2
            assert df.iloc[1]["Risk"] == "New risk"
            assert df.iloc[1]["Issue"] == "#124"
            assert df.iloc[1]["Updates"] == "#124"
            assert df.iloc[1]["Reach"] == "Very High"
            assert pd.isna(df.iloc[1]["Maintainer Notes"]) or df.iloc[1]["Maintainer Notes"] == ""
