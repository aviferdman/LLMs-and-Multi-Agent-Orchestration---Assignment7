#!/usr/bin/env python3
"""Launch the Streamlit GUI dashboard."""
import subprocess
import sys


def main():
    """Run the Streamlit GUI application."""
    cmd = [sys.executable, "-m", "streamlit", "run", "gui/app.py", "--server.port", "8501"]
    subprocess.run(cmd)


if __name__ == "__main__":
    main()
