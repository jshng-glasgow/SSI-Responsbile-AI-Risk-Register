import pytest
import pandas as pd
import os
import sys
from io import StringIO
from unittest.mock import patch

# Add the scripts directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '.github', 'scripts'))

from validate_csv import validate, REQUIRED_COLUMNS, VALID_LEVELS

class TestValidateCSV:
    def test_valid_csv(self, tmp_path):
        # Create a valid CSV
        csv_content = """Risk,Likelihood,Severity,Mitigations,Ownership,Examples,Issue
"Test risk",High,Medium,"Mitigation text","Owner","Examples","#1"
"""
        register_dir = tmp_path / "register"
        register_dir.mkdir()
        csv_file = register_dir / "risks.csv"
        csv_file.write_text(csv_content)
        
        # Change to tmp_path for relative path
        original_cwd = os.getcwd()
        os.chdir(tmp_path)
        try:
            with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
                validate()
                output = mock_stdout.getvalue()
                assert "CSV valid — 1 risks in register" in output
        finally:
            os.chdir(original_cwd)

    def test_missing_columns(self, tmp_path):
        csv_content = """Risk,Likelihood,Mitigations
"Test risk",High,"Mitigation"
"""
        register_dir = tmp_path / "register"
        register_dir.mkdir()
        csv_file = register_dir / "risks.csv"
        csv_file.write_text(csv_content)
        
        original_cwd = os.getcwd()
        os.chdir(tmp_path)
        try:
            with pytest.raises(SystemExit):
                with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
                    validate()
                    output = mock_stdout.getvalue()
                    assert "Missing columns:" in output
        finally:
            os.chdir(original_cwd)

    def test_empty_required_field(self, tmp_path):
        csv_content = """Risk,Likelihood,Severity,Mitigations,Ownership,Examples,Issue
"",High,Medium,"Mitigation","Owner","Examples","#1"
"""
        register_dir = tmp_path / "register"
        register_dir.mkdir()
        csv_file = register_dir / "risks.csv"
        csv_file.write_text(csv_content)
        
        original_cwd = os.getcwd()
        os.chdir(tmp_path)
        try:
            with pytest.raises(SystemExit):
                with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
                    validate()
                    output = mock_stdout.getvalue()
                    assert "has empty values" in output
        finally:
            os.chdir(original_cwd)

    def test_invalid_likelihood(self, tmp_path):
        csv_content = """Risk,Likelihood,Severity,Mitigations,Ownership,Examples,Issue
"Test risk",Invalid,Medium,"Mitigation","Owner","Examples","#1"
"""
        register_dir = tmp_path / "register"
        register_dir.mkdir()
        csv_file = register_dir / "risks.csv"
        csv_file.write_text(csv_content)
        
        original_cwd = os.getcwd()
        os.chdir(tmp_path)
        try:
            with pytest.raises(SystemExit):
                with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
                    validate()
                    output = mock_stdout.getvalue()
                    assert "Invalid values in 'Likelihood'" in output
        finally:
            os.chdir(original_cwd)

    def test_invalid_severity(self, tmp_path):
        csv_content = """Risk,Likelihood,Severity,Mitigations,Ownership,Examples,Issue
"Test risk",High,Invalid,"Mitigation","Owner","Examples","#1"
"""
        register_dir = tmp_path / "register"
        register_dir.mkdir()
        csv_file = register_dir / "risks.csv"
        csv_file.write_text(csv_content)
        
        original_cwd = os.getcwd()
        os.chdir(tmp_path)
        try:
            with pytest.raises(SystemExit):
                with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
                    validate()
                    output = mock_stdout.getvalue()
                    assert "Invalid values in 'Severity'" in output
        finally:
            os.chdir(original_cwd)