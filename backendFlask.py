from flask import Flask
#jsonify: use later for result in frontend
#request?

import subprocess #to run with same interpreter
import sys
from pathlib import Path


app = Flask(__name__)

ROOT = Path(__file__).resolve().parent
SCRIPT = ROOT / "channelLoader.py"

@app.route("/run", methods=["POST"])
def run_script():

    result = subprocess.run(
        [sys.executable, str(SCRIPT)],
        cwd=str(ROOT),
        capture_output=True,
        text=True
    )
    
    if result.returncode != 0:
        return "Script failed:\n" + result.stderr, 500

    return "Script ran successfully:\n" + result.stdout, 200

