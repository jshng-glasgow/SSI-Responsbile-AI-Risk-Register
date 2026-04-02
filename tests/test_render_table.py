import pytest
import pandas as pd
import os
import sys
import json
from bs4 import BeautifulSoup

# Add the scripts directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '.github', 'scripts'))

# Import the script - it runs on import, so we need to be careful
# Instead, we'll run it in tests

class TestRenderTable:
    def test_render_table_creates_html(self, tmp_path):
        # Create a test CSV
        csv_content = """Risk,Likelihood,Severity,Reach,Mitigations,Ownership,Examples,Issue,Updates,Maintainer Notes
"Test risk",High,Medium,Low,"Mitigation text","Owner","Examples","#1","#1",""
"Another risk",Low,High,Very High,"Another mitigation","Another owner","Another examples","#2","#2, #5","Synthesised from issues #2 and #5"
"""
        csv_file = tmp_path / "register" / "risks.csv"
        csv_file.parent.mkdir()
        csv_file.write_text(csv_content)
        
        html_file = tmp_path / "docs" / "index.html"
        json_file = tmp_path / "docs" / "risks.json"
        
        # Change to tmp_path
        original_cwd = os.getcwd()
        os.chdir(tmp_path)
        try:
            # Import and run the script
            script_path = os.path.join(original_cwd, '.github', 'scripts', 'render_table.py')
            with open(script_path, 'r') as f:
                script_code = f.read()
            # Set __name__ to __main__ to run the code
            exec(script_code, {'__name__': '__main__'})
            
            # Check HTML file was created
            assert html_file.exists()
            assert json_file.exists()
            
            # Check content
            with open(str(html_file), 'r', encoding='utf-8') as f:
                html_content = f.read()

            with open(str(json_file), 'r', encoding='utf-8') as f:
                json_content = json.load(f)
            
            # Parse HTML
            soup = BeautifulSoup(html_content, 'html.parser')
            
            # Check title
            assert soup.title.string == "SSI Generative AI Risk Register"
            
            # Check app shell exists
            assert soup.find(id="register-root") is not None
            assert soup.find(id="search-input") is not None
            assert soup.find("script", src="./app.js") is not None

            # Check JSON structure
            assert len(json_content) == 2
            assert json_content[0]["Risk"] == "Test risk"
            assert json_content[0]["Likelihood"] == "High"
            assert json_content[0]["Severity"] == "Medium"
            assert json_content[0]["Reach"] == "Low"
            assert json_content[0]["issue_url"].endswith("/issues/1")
            assert json_content[1]["update_urls"][1]["label"] == "#5"
            
        finally:
            os.chdir(original_cwd)

    def test_render_table_with_newlines(self, tmp_path):
        # Create CSV with newlines
        csv_content = """Risk,Likelihood,Severity,Reach,Mitigations,Ownership,Examples,Issue,Updates,Maintainer Notes
"Test risk\nwith newline",High,Medium,Low,"Mitigation\ntext","Owner","Examples","#1","#1",""
"""
        csv_file = tmp_path / "register" / "risks.csv"
        csv_file.parent.mkdir()
        csv_file.write_text(csv_content)
        
        html_file = tmp_path / "docs" / "index.html"
        json_file = tmp_path / "docs" / "risks.json"
        
        original_cwd = os.getcwd()
        os.chdir(tmp_path)
        try:
            script_path = os.path.join(original_cwd, '.github', 'scripts', 'render_table.py')
            with open(script_path, 'r') as f:
                script_code = f.read()
            exec(script_code, {'__name__': '__main__'})
            
            with open(str(html_file), 'r', encoding='utf-8') as f:
                html_content = f.read()

            with open(str(json_file), 'r', encoding='utf-8') as f:
                json_content = json.load(f)
            
            # Check the app shell renders and JSON keeps the content
            assert "register-root" in html_content
            assert "with newline" in json_content[0]["Risk"]
            assert json_content[0]["Mitigations"].replace("\r\n", "\n") == "Mitigation\ntext"
            
        finally:
            os.chdir(original_cwd)
