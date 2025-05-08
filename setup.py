import os

# Define your project structure
folders = [
    "scraper",
    "data",
    "notebooks",
    "analysis",
    "dashboard",
    "alerts"
]

files = {
    "requirements.txt": "",
    "README.md": "# Insider Intel — Tracking Real Insider Trades for Hidden Alpha",
    "scraper/insider_scraper.py": "# Scraper code will go here"
}

# Create folders
for folder in folders:
    os.makedirs(folder, exist_ok=True)
    print(f"Created folder: {folder}")

# Create files
for filepath, content in files.items():
    with open(filepath, "w") as f:
        f.write(content)
    print(f"Created file: {filepath}")

print("\n✅ Project folder structure is ready!")
