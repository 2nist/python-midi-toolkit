#!/usr/bin/env python3
"""
Simple test script to verify Python environment from REAPER
"""
import sys
import os
import json

def main():
    result = {
        "test": "success",
        "python_version": sys.version,
        "python_executable": sys.executable,
        "working_directory": os.getcwd(),
        "script_path": __file__,
        "env_path": os.environ.get("PATH", ""),
        "pythonpath": os.environ.get("PYTHONPATH", "")
    }
    
    print(json.dumps(result, indent=2))

if __name__ == "__main__":
    main()
