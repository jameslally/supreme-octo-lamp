#!/usr/bin/env python3
"""
Simple script to run the CLI from the new package structure.
"""

import sys
import os
from pathlib import Path

def main():
    """Run the CLI."""
    # Get the absolute path to the project root
    project_root = Path(__file__).parent.absolute()
    
    # Change to the project root directory so imports work correctly
    os.chdir(project_root)
    
    # Add the src directory to the path
    src_path = str(project_root / "src")
    if src_path not in sys.path:
        sys.path.insert(0, src_path)
    
    # Import and run the CLI
    try:
        from cli import main as cli_main
        cli_main()
    except ImportError as e:
        print(f"❌ Failed to import CLI: {e}")
        print(f"📁 Current working directory: {os.getcwd()}")
        print(f"📁 Python path: {sys.path[:3]}...")  # Show first 3 paths
        return 1
    except Exception as e:
        print(f"❌ CLI execution failed: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
