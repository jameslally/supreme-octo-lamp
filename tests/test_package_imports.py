#!/usr/bin/env python3
"""
Test that the package imports work correctly after refactoring.
"""

import sys
import os

# Add the src directory to the path for testing
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

def test_package_imports():
    """Test that we can import the main package components."""
    try:
        from job_requirements_extractor import JobRequirementsExtractor, BatchJobProcessor
        from job_requirements_extractor import (
            DEFAULT_MODEL,
            NER_CONFIDENCE_THRESHOLD,
            REQUIREMENT_PATTERNS,
            REQUIREMENT_CATEGORIES
        )
        print("✅ Package imports successful!")
        return True
    except ImportError as e:
        print(f"❌ Package import failed: {e}")
        return False

def test_extractor_instantiation():
    """Test that we can create an instance of the extractor."""
    try:
        from job_requirements_extractor import JobRequirementsExtractor
        extractor = JobRequirementsExtractor()
        print("✅ Extractor instantiation successful!")
        return True
    except Exception as e:
        print(f"❌ Extractor instantiation failed: {e}")
        return False

if __name__ == "__main__":
    print("Testing package imports...")
    test_package_imports()
    test_extractor_instantiation()
    print("Package import tests completed!")
