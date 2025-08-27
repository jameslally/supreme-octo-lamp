#!/usr/bin/env python3
"""
Test the package structure without requiring external dependencies.
"""

import os
import sys
from pathlib import Path

def test_directory_structure():
    """Test that the expected directory structure exists."""
    print("Testing directory structure...")
    
    # Check that src directory exists
    src_path = Path("src")
    assert src_path.exists(), "src directory should exist"
    assert src_path.is_dir(), "src should be a directory"
    
    # Check that tests directory exists
    tests_path = Path("tests")
    assert tests_path.exists(), "tests directory should exist"
    assert tests_path.is_dir(), "tests should be a directory"
    
    # Check that package directory exists
    package_path = src_path / "job_requirements_extractor"
    assert package_path.exists(), "job_requirements_extractor package should exist"
    assert package_path.is_dir(), "job_requirements_extractor should be a directory"
    
    # Check that __init__.py exists in package
    init_file = package_path / "__init__.py"
    assert init_file.exists(), "__init__.py should exist in package"
    
    # Check that main modules exist
    extractor_file = package_path / "extractor.py"
    assert extractor_file.exists(), "extractor.py should exist in package"
    
    batch_processor_file = package_path / "batch_processor.py"
    assert batch_processor_file.exists(), "batch_processor.py should exist in package"
    
    config_file = package_path / "config.py"
    assert config_file.exists(), "config.py should exist in package"
    
    # Check that entry points exist
    app_file = src_path / "app.py"
    assert app_file.exists(), "app.py should exist in src"
    
    cli_file = src_path / "cli.py"
    assert cli_file.exists(), "cli.py should exist in src"
    
    print("✅ Directory structure is correct!")

def test_package_files():
    """Test that package files contain expected content."""
    print("Testing package files...")
    
    # Check __init__.py has expected imports
    init_file = Path("src/job_requirements_extractor/__init__.py")
    with open(init_file, 'r') as f:
        content = f.read()
        assert "JobRequirementsExtractor" in content, "__init__.py should export JobRequirementsExtractor"
        assert "BatchJobProcessor" in content, "__init__.py should export BatchJobProcessor"
    
    # Check that setup.py exists
    setup_file = Path("setup.py")
    assert setup_file.exists(), "setup.py should exist"
    
    # Check that pyproject.toml exists
    pyproject_file = Path("pyproject.toml")
    assert pyproject_file.exists(), "pyproject.toml should exist"
    
    # Check that pytest.ini exists
    pytest_file = Path("pytest.ini")
    assert pytest_file.exists(), "pytest.ini should exist"
    
    print("✅ Package files are correct!")

def test_test_files():
    """Test that test files exist."""
    print("Testing test files...")
    
    tests_path = Path("tests")
    
    # Check that test files exist
    test_files = list(tests_path.glob("test_*.py"))
    assert len(test_files) > 0, "Should have at least one test file"
    
    # Check that our structure test exists
    structure_test = tests_path / "test_structure.py"
    assert structure_test.exists(), "test_structure.py should exist"
    
    print(f"✅ Found {len(test_files)} test files!")

def main():
    """Run all structure tests."""
    print("🏗️  Testing package structure...")
    
    try:
        test_directory_structure()
        test_package_files()
        test_test_files()
        print("\n🎉 All structure tests passed!")
        return True
    except AssertionError as e:
        print(f"\n❌ Structure test failed: {e}")
        return False
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
