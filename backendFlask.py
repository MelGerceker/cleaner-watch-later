from flask import Flask
from flask import send_from_directory
from flask import jsonify

#request?

import subprocess #to run with same interpreter
import sys
from pathlib import Path


app = Flask(__name__)

ROOT = Path(__file__).resolve().parent
SCRIPT = ROOT / "channelLoader.py"

@app.route("/")
def index():
    return send_from_directory(ROOT,"index.html")

@app.route("/run", methods=["POST"])
def run_script():

    result = subprocess.run(
        [sys.executable, str(SCRIPT)],
        cwd=str(ROOT),
        capture_output=True,
        text=True
    )
    
    if result.returncode != 0:
        return jsonify({
            "success": False,
            "error": result.stderr
        }), 500

    return jsonify({
        "success": True,
        "output": result.stdout
    })

if __name__ == "__main__":
    app.run(debug=True)

#have to choose between flask vs live server
#currently live server does not get the update button request
#currently flask can not access css and javascript files and it needs cors