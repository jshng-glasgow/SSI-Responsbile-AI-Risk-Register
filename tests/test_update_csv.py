import pytest
import pandas as pd
import os
import sys
from unittest.mock import patch, MagicMock

# Add the scripts directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '.github', 'scripts'))

from update_csv import parse_issue, update_csv_row, FIELDS, CSV_PATH

class TestUpdateCSV:
    def test_parse_issue_complete(self):
        body = """### Issue Number
#123

### Risk
Updated risk description

### Likelihood
High

### Severity
Medium

### Mitigations
Updated mitigations

### Ownership
Updated owner

### Examples
Updated examples
"""
        values = parse_issue(body)
        assert values["Issue Number"] == "#123"
        assert values["Risk"] == "Updated risk description"
        assert values["Likelihood"] == "High"
        assert values["Severity"] == "Medium"
        assert values["Mitigations"] == "Updated mitigations"
        assert values["Ownership"] == "Updated owner"
        assert values["Examples"] == "Updated examples"

    def test_parse_issue_none_values(self):
        body = """### Issue Number
#123

### Risk
Updated risk

### Likelihood
None

### Severity
_No response_

### Mitigations

### Ownership
None

### Examples
Examples
"""
        values = parse_issue(body)
        assert values["Issue Number"] == "#123"
        assert values["Risk"] == "Updated risk"
        assert values["Likelihood"] is None
        assert values["Severity"] is None
        assert values["Mitigations"] is None
        assert values["Ownership"] is None
        assert values["Examples"] == "Examples"

    def test_update_csv_row_success(self, tmp_path):
        test_csv = tmp_path / "risks.csv"
        # Create existing CSV
        existing_df = pd.DataFrame({
            "Risk": ["Original risk"],
            "Likelihood": ["Low"],
            "Severity": ["High"],
            "Mitigations": ["Original mitigations"],
            "Ownership": ["Original owner"],
            "Examples": ["Original examples"],
            "Issue": ["#123"],
            "Updates": ["#123"]
        })
        existing_df.to_csv(str(test_csv), index=False)
        
        with patch('update_csv.CSV_PATH', str(test_csv)):
            values = {
                "Issue Number": "#123",
                "Risk": "Updated risk",
                "Likelihood": None,  # Should not update
                "Severity": "Medium",  # Should update
                "Mitigations": None,
                "Ownership": "Updated owner",
                "Examples": None
            }
            update_csv_row(values, "999")
            
            df = pd.read_csv(str(test_csv))
            assert len(df) == 1
            assert df.iloc[0]["Risk"] == "Updated risk"
            assert df.iloc[0]["Likelihood"] == "Low"  # Unchanged
            assert df.iloc[0]["Severity"] == "Medium"  # Updated
            assert df.iloc[0]["Mitigations"] == "Original mitigations"  # Unchanged
            assert df.iloc[0]["Ownership"] == "Updated owner"  # Updated
            assert df.iloc[0]["Examples"] == "Original examples"  # Unchanged
            # Updates should have the update issue appended
            assert "#999" in str(df.iloc[0]["Updates"])

    def test_update_csv_row_issue_not_found(self, tmp_path):
        test_csv = tmp_path / "risks.csv"
        # Create existing CSV
        existing_df = pd.DataFrame({
            "Risk": ["Original risk"],
            "Likelihood": ["Low"],
            "Severity": ["High"],
            "Mitigations": ["Original mitigations"],
            "Ownership": ["Original owner"],
            "Examples": ["Original examples"],
            "Issue": ["#123"],
            "Updates": ["#123"]
        })
        existing_df.to_csv(str(test_csv), index=False)
        
        with patch('update_csv.CSV_PATH', str(test_csv)):
            values = {
                "Issue Number": "#999",  # Non-existent
                "Risk": "Updated risk"
            }
            with pytest.raises(SystemExit):
                update_csv_row(values, "888")

    def test_update_csv_row_no_csv(self, tmp_path):
        test_csv = tmp_path / "nonexistent.csv"
        
        with patch('update_csv.CSV_PATH', str(test_csv)):
            values = {
                "Issue Number": "#123",
                "Risk": "Updated risk"
            }
            with pytest.raises(SystemExit):
                update_csv_row(values, "777")