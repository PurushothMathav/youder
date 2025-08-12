__author__ = 'Mr. Pangu'

import requests
import tempfile
import subprocess
import sys
import os

GITHUB_RAW_URL = "https://gist.githubusercontent.com/PurushothMathav/d052714fa6a829d1d9502bf6063bf10d/raw/cde98241df6cd5028548afac52a81b5f2fb5ef70/youder_v2.py"

print("Downloading the latest Youder source from GitHub...")
response = requests.get(GITHUB_RAW_URL)
response.raise_for_status()

with tempfile.NamedTemporaryFile(delete=False, suffix=".py") as tmp_file:
    tmp_file.write(response.content)
    tmp_path = tmp_file.name

print(f"Running Youder from: {tmp_path}")
subprocess.run([sys.executable, tmp_path])


os.remove(tmp_path)

