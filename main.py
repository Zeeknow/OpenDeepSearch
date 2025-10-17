#!/usr/bin/env python3
"""
Safe DeFi Assistant - Main Entry Point
Clean Architecture Implementation
"""

import os
import sys
from pathlib import Path

# Add the project root to Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from apps.web.defi_assistant_server import main

if __name__ == "__main__":
    main()
