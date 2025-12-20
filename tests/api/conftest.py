"""Pytest configuration for API tests."""

import os
import sys
from pathlib import Path

# Add project root to Python path at the very beginning
project_root = Path(__file__).parent.parent.parent.resolve()
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

# Also set PYTHONPATH environment variable
os.environ['PYTHONPATH'] = str(project_root)
