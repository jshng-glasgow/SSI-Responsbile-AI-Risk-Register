import pandas as pd
import os

CSV_PATH = "register/risks.csv"
OUTPUT_PATH = "docs/index.html"

os.makedirs("docs", exist_ok=True)

df = pd.read_csv(CSV_PATH)
# Convert newlines to HTML line breaks
df = df.apply(lambda col: col.str.replace('\n', '<br>', regex=False))

#html_table = df.to_html(index=False, classes='risk-table', escape=False)

html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>SSI Generative AI Risk Register</title>
    <style>
        body {{
            font-family: sans-serif;
            max-width: 1200px;
            margin: 40px auto;
            padding: 0 20px;
            color: #333;
        }}
        table {{
            width: 100%;
            border-collapse: collapse;
            font-size: 0.9em;
        }}
        th {{
            background-color: #2c3e50;
            color: white;
            padding: 10px;
            text-align: left;
        }}
        td {{
            padding: 10px;
            border: 1px solid #ddd;
            vertical-align: top;
            white-space: normal;
            word-wrap: break-word;
        }}
        tr:nth-child(even) {{
            background-color: #f9f9f9;
        }}
        .high {{ color: #c0392b; font-weight: bold; }}
        .medium {{ color: #e67e22; font-weight: bold; }}
        .low {{ color: #27ae60; font-weight: bold; }}
        .unknown {{ color: #7f8c8d; font-weight: bold; }}
    </style>
</head>
<body>
    <h1>SSI Generative AI Risk Register</h1>
    <p>A community-maintained register of risks associated with the use of AI in Research Software Engineering.
    Contribute via <a href="https://github.com/jshng-glasgow/SSI-Responsible-AI-Risk-Register/">GitHub</a>.</p>
    {df.to_html(index=False, classes='risk-table', escape=False)}
</body>
</html>"""

with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
    f.write(html)

print(f"Generated {OUTPUT_PATH}")