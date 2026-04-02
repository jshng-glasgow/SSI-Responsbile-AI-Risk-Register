import pytest
import pandas as pd
import os
import sys
from bs4 import BeautifulSoup

# Add the scripts directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '.github', 'scripts'))

# Import the script - it runs on import, so we need to be careful
# Instead, we'll run it in tests

class TestRenderTable:
    def test_render_table_creates_html(self, tmp_path):
        # Create a test CSV
        csv_content = """Risk,Likelihood,Severity,Reach,Mitigations,Ownership,Examples,Issue,Maintainer Notes
"Test risk",High,Medium,Low,"Mitigation text","Owner","Examples","#1",""
"Another risk",Low,High,Very High,"Another mitigation","Another owner","Another examples","#2","Synthesised from issues #2 and #5"
"""
        csv_file = tmp_path / "register" / "risks.csv"
        csv_file.parent.mkdir()
        csv_file.write_text(csv_content)
        
        html_file = tmp_path / "docs" / "index.html"
        
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
            
            # Check content
            with open(str(html_file), 'r', encoding='utf-8') as f:
                html_content = f.read()
            
            # Parse HTML
            soup = BeautifulSoup(html_content, 'html.parser')
            
            # Check title
            assert soup.title.string == "SSI Generative AI Risk Register"
            
            # Check table exists
            table = soup.find('table')
            assert table is not None
            
            # Check rows (header + 2 data rows)
            rows = table.find_all('tr')
            assert len(rows) == 3
            
            # Check first data row
            first_data_row = rows[1]
            cells = first_data_row.find_all('td')
            assert cells[0].text == "Test risk"
            assert cells[1].text == "High"
            assert cells[2].text == "Medium"
            assert cells[3].text == "Low"
            
        finally:
            os.chdir(original_cwd)

    def test_render_table_with_newlines(self, tmp_path):
        # Create CSV with newlines
        csv_content = """Risk,Likelihood,Severity,Reach,Mitigations,Ownership,Examples,Issue,Maintainer Notes
"Test risk\nwith newline",High,Medium,Low,"Mitigation\ntext","Owner","Examples","#1",""
"""
        csv_file = tmp_path / "register" / "risks.csv"
        csv_file.parent.mkdir()
        csv_file.write_text(csv_content)
        
        html_file = tmp_path / "docs" / "index.html"
        
        original_cwd = os.getcwd()
        os.chdir(tmp_path)
        try:
            script_path = os.path.join(original_cwd, '.github', 'scripts', 'render_table.py')
            with open(script_path, 'r') as f:
                script_code = f.read()
            exec(script_code, {'__name__': '__main__'})
            
            with open(str(html_file), 'r', encoding='utf-8') as f:
                html_content = f.read()
            
            # Check newlines are present (may or may not be converted to <br>)
            assert "Test risk" in html_content
            assert "with newline" in html_content
            
        finally:
            os.chdir(original_cwd)
