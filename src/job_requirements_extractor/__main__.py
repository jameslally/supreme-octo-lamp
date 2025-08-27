#!/usr/bin/env python3
"""
Main entry point for the job_requirements_extractor package.
"""

import sys
import os

# Add the src directory to the path so we can import the CLI
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from cli import main

if __name__ == "__main__":
    main()
