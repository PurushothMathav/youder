import requests
import tempfile
import subprocess
import sys
import os

GITHUB_RAW_URL = "https://raw.githubusercontent.com/<username>/<repo>/main/script.py"

print("Downloading the latest Youder source from GitHub...")
response = requests.get(GITHUB_RAW_URL)
response.raise_for_status()

with tempfile.NamedTemporaryFile(delete=False, suffix=".py") as tmp_file:
    tmp_file.write(response.content)
    tmp_path = tmp_file.name

print(f"Running Youder from: {tmp_path}")
subprocess.run([sys.executable, tmp_path])


os.remove(tmp_path)
