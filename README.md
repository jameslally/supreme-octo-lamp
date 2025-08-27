# Job Requirements Extractor

A comprehensive tool for extracting and analyzing requirements from job descriptions using advanced NLP techniques including Named Entity Recognition and pattern matching.

## 🏗️ Project Structure

The project has been refactored into a proper Python package structure:

```
supreme-octo-lamp/
├── src/
│   ├── job_requirements_extractor/     # Main package
│   │   ├── __init__.py                # Package initialization
│   │   ├── __main__.py                # Module entry point
│   │   ├── extractor.py               # Core extraction logic
│   │   ├── batch_processor.py         # Batch processing functionality
│   │   └── config.py                  # Configuration and constants
│   ├── app.py                         # Streamlit web application
│   └── cli.py                         # Command-line interface
├── tests/                             # Test files
│   ├── test_package_imports.py        # Package structure tests
│   ├── test_improved.py               # Improved extraction tests
│   └── test_sentence_extraction.py    # Sentence extraction tests
├── setup.py                           # Package setup configuration
├── pyproject.toml                     # Modern Python packaging config
├── pytest.ini                         # Test configuration
├── run_app.py                         # Streamlit app runner
├── run_cli.py                         # CLI runner
└── requirements.txt                    # Python dependencies
```

## 🚀 Quick Start

### Installation

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd supreme-octo-lamp
   ```

2. **Create a virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Install the package in development mode:**
   ```bash
   pip install -e .
   ```

### Usage

#### Web Application (Streamlit)

Run the Streamlit web application:

```bash
# Option 1: Use the runner script
python run_app.py

# Option 2: Run directly with streamlit
streamlit run src/app.py

# Option 3: Run as a module
python -m streamlit run src/app.py
```

#### Command Line Interface

Use the CLI for batch processing and automation:

```bash
# Option 1: Use the runner script
python run_cli.py

# Option 2: Run directly
python src/cli.py

# Option 3: Use the installed command (after pip install -e .)
job-extractor

# Examples:
python src/cli.py -t "We are looking for a Python developer with 3+ years experience"
python src/cli.py -f job_description.txt -o results.json
```

#### Python Package

Import and use the package in your own code:

```python
from job_requirements_extractor import JobRequirementsExtractor

# Create an extractor instance
extractor = JobRequirementsExtractor()

# Extract requirements from job description
job_description = "We are looking for a Python developer..."
requirements = extractor.extract_requirements(job_description)

print(requirements)
```

## 🧪 Testing

Run the test suite:

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src/job_requirements_extractor

# Run specific test file
pytest tests/test_package_imports.py
```

## 📦 Package Development

### Building the Package

```bash
# Build source distribution
python setup.py sdist

# Build wheel
python setup.py bdist_wheel
```

### Installing in Development Mode

```bash
pip install -e .
```

This allows you to modify the source code and see changes immediately without reinstalling.

## 🔧 Configuration

The package configuration is centralized in `src/job_requirements_extractor/config.py`. Key settings include:

- `DEFAULT_MODEL`: Default Hugging Face model for extraction
- `NER_CONFIDENCE_THRESHOLD`: Minimum confidence for entity extraction
- `REQUIREMENT_PATTERNS`: Regex patterns for requirement detection
- `REQUIREMENT_CATEGORIES`: Categories for organizing requirements

## 📚 API Reference

### JobRequirementsExtractor

Main class for extracting requirements from job descriptions.

**Methods:**
- `extract_requirements(job_description)`: Extract all requirements
- `_extract_text_patterns(text)`: Extract requirements using regex patterns
- `_extract_entities(text)`: Extract named entities using NER
- `_categorize_requirements(text)`: Categorize requirements by type

### BatchJobProcessor

Process multiple job descriptions in batch.

**Methods:**
- `process_files(file_paths)`: Process multiple files
- `process_texts(texts)`: Process multiple text strings
- `save_results(results, output_file)`: Save results to file

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Run the test suite
6. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

If you encounter any issues or have questions:

1. Check the existing issues
2. Create a new issue with detailed information
3. Include error messages and reproduction steps

## 🔄 Migration from Old Structure

If you were using the old structure with files in the root directory:

- **Old import:** `from job_requirements_extractor import JobRequirementsExtractor`
- **New import:** `from job_requirements_extractor import JobRequirementsExtractor` (same!)

The package structure maintains backward compatibility while providing better organization and installability.
