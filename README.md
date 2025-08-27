# 💼 Job Requirements Extractor

An intelligent Python application that uses Hugging Face models to automatically extract and analyze requirements from job descriptions. Built with modern NLP techniques including Named Entity Recognition (NER), pattern matching, and semantic analysis.

## ✨ Features

- **🤖 AI-Powered Extraction**: Uses state-of-the-art Hugging Face models for accurate requirement identification
- **🔍 Multiple Extraction Methods**: Combines regex patterns, NER, and semantic analysis
- **🏷️ Smart Categorization**: Automatically organizes requirements into logical categories
- **📊 Comprehensive Analysis**: Provides complexity scores, requirement density, and insights
- **💡 Personalized Recommendations**: Offers actionable advice based on extracted requirements
- **🌐 Multiple Interfaces**: Web app (Streamlit), command-line, and Python library
- **💾 Export Results**: Save analysis results in JSON format

## 🚀 Quick Start

### Installation

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd job_matcher
   ```


2. **Install dependencies:**
   ```bash
   python -m venv venv
   source venv/bin/activate    # macOS/Linux
   venv\Scripts\activate       # Windows
   pip install -r requirements.txt
   ```

3. **Run the web application:**
   ```bash
   streamlit run app.py
   ```

4. **Or use the command-line interface:**
   ```bash
   python cli.py -t "We are looking for a Python developer with 3+ years experience"
   ```

## 🎯 Use Cases

- **Job Seekers**: Analyze job requirements to optimize resumes and applications
- **HR Professionals**: Review and standardize job postings
- **Career Counselors**: Provide data-driven guidance to clients
- **Recruiters**: Quickly assess candidate-job fit
- **Researchers**: Analyze job market trends and requirements

## 🏗️ Architecture

The application uses a modular architecture with three main components:

### 1. Core Extractor (`job_requirements_extractor.py`)
- **JobRequirementsExtractor Class**: Main extraction engine
- **Multiple Extraction Methods**: Pattern matching, NER, categorization
- **Text Processing**: Cleaning, preprocessing, and analysis
- **Complexity Scoring**: Algorithmic assessment of job difficulty

### 2. Web Interface (`app.py`)
- **Streamlit Application**: User-friendly web interface
- **Interactive Features**: File upload, real-time analysis, visualizations
- **Responsive Design**: Works on desktop and mobile devices
- **Results Export**: Download analysis in JSON format

### 3. Command Line Interface (`cli.py`)
- **CLI Tool**: Terminal-based usage
- **File Processing**: Analyze text files and save results
- **Batch Processing**: Handle multiple job descriptions
- **Verbose Output**: Detailed analysis information

## 🔧 Configuration

### Model Selection
The application supports multiple Hugging Face models:

- **Default NER Model**: `dbmdz/bert-large-cased-finetuned-conll03-english`
- **Alternative Models**: `microsoft/DialoGPT-medium` and others
- **Custom Models**: Use any compatible Hugging Face model

### Confidence Thresholds
- **Entity Confidence**: Minimum score for NER entities (default: 0.7)
- **Pattern Matching**: Configurable regex patterns for requirements
- **Semantic Analysis**: Adjustable similarity thresholds

## 📊 Output Format

The application generates comprehensive analysis results:

```json
{
  "requirements": {
    "text_requirements": ["5+ years of experience", "Python proficiency"],
    "entity_requirements": [{"text": "Python", "type": "SKILL", "confidence": 0.95}],
    "categorized_requirements": {
      "technical_skills": ["Python", "Java", "AWS"],
      "experience": ["5+ years", "senior level"],
      "education": ["Bachelor's degree"]
    },
    "summary": {
      "total_sentences": 15,
      "requirement_sentences": 8,
      "requirement_density": 0.53,
      "estimated_requirements": 12
    }
  },
  "text_length": 1250,
  "word_count": 200,
  "complexity_score": 7.2,
  "recommendations": [
    "Focus on highlighting relevant technical skills in your resume",
    "Emphasize relevant work experience and achievements"
  ]
}
```

## 🎨 Web Interface Features

### Input Methods
- **Text Input**: Paste job descriptions directly
- **File Upload**: Support for .txt, .md files
- **Sample Data**: Built-in examples for testing

### Visualization
- **Metrics Dashboard**: Key statistics at a glance
- **Interactive Charts**: Requirement density and analysis summary
- **Responsive Layout**: Optimized for all screen sizes

### Export Options
- **JSON Download**: Complete analysis results
- **Raw Data View**: Expandable detailed information
- **Formatted Display**: Clean, organized presentation

## 💻 Command Line Usage

### Basic Commands

```bash
# Analyze text from command line
python cli.py -t "We are looking for a Python developer with 3+ years experience"

# Analyze text from file
python cli.py -f job_description.txt

# Save results to file
python cli.py -f job_description.txt -o results.json

# Verbose output
python cli.py -f job_description.txt -v

# Use custom model
python cli.py -f job_description.txt --model custom-model-name

# Adjust confidence threshold
python cli.py -f job_description.txt --confidence 0.8
```

### Command Line Options

| Option | Description | Default |
|--------|-------------|---------|
| `-t, --text` | Job description text | - |
| `-f, --file` | Input file path | - |
| `-o, --output` | Output JSON file | - |
| `-v, --verbose` | Verbose output | False |
| `--model` | Hugging Face model | dbmdz/bert-large-cased-finetuned-conll03-english |
| `--confidence` | Entity confidence threshold | 0.7 |

## 🔬 Technical Details

### NLP Techniques Used

1. **Named Entity Recognition (NER)**
   - BERT-based model for entity extraction
   - Identifies skills, experience levels, qualifications
   - Configurable confidence thresholds

2. **Pattern Matching**
   - Regex patterns for common requirement formats
   - Years of experience, education levels, skill requirements
   - Customizable pattern library

3. **Semantic Analysis**
   - Sentence transformers for similarity matching
   - Requirement categorization and clustering
   - Context-aware analysis

4. **Text Processing**
   - Advanced text cleaning and preprocessing
   - Sentence segmentation and analysis
   - Complexity scoring algorithms

### Performance Optimization

- **GPU Acceleration**: Automatic CUDA detection and usage
- **Model Caching**: Efficient model loading and reuse
- **Batch Processing**: Handle multiple documents efficiently
- **Memory Management**: Optimized for large text processing

## 🚧 Requirements

### System Requirements
- **Python**: 3.8 or higher
- **Memory**: 4GB RAM minimum (8GB recommended)
- **Storage**: 2GB free space for models
- **GPU**: Optional but recommended for faster processing

### Dependencies
- **Core**: transformers, torch, sentence-transformers
- **Web**: streamlit, plotly, pandas
- **Utilities**: numpy, scikit-learn, python-dotenv

## 📈 Performance Benchmarks

| Text Length | Processing Time | Memory Usage |
|-------------|----------------|--------------|
| 1,000 chars | ~2-3 seconds | ~500MB |
| 5,000 chars | ~5-8 seconds | ~800MB |
| 10,000 chars | ~10-15 seconds | ~1.2GB |

*Benchmarks on CPU (Intel i7), GPU performance significantly faster*

## 🔒 Security & Privacy

- **Local Processing**: All analysis happens locally
- **No Data Transmission**: Job descriptions never leave your system
- **Model Safety**: Uses only verified Hugging Face models
- **Input Validation**: Robust error handling and validation

## 🤝 Contributing

We welcome contributions! Please see our contributing guidelines:

1. **Fork the repository**
2. **Create a feature branch**
3. **Make your changes**
4. **Add tests if applicable**
5. **Submit a pull request**

### Development Setup

```bash
# Clone and setup
git clone <repository-url>
cd job_matcher

# Install development dependencies
pip install -r requirements.txt
pip install pytest black flake8

# Run tests
pytest

# Format code
black .

# Lint code
flake8
```

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **Hugging Face**: For providing excellent NLP models and libraries
- **Streamlit**: For the amazing web framework
- **Open Source Community**: For continuous improvements and feedback

## 📞 Support

- **Issues**: Report bugs and feature requests on GitHub
- **Documentation**: Check the code comments and docstrings
- **Community**: Join our discussions and share your use cases

## 🔮 Future Roadmap

- **Multi-language Support**: Analyze job descriptions in different languages
- **Resume Matching**: Compare candidate resumes with job requirements
- **Market Analysis**: Aggregate and analyze job market trends
- **API Service**: RESTful API for integration with other systems
- **Mobile App**: Native mobile applications
- **Advanced Analytics**: Machine learning insights and predictions

---

**Made with ❤️ for the job matching community**
