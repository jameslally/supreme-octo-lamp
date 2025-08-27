"""
Configuration file for Job Requirements Extractor
"""

import os
from typing import List, Dict, Any

# Model Configuration
DEFAULT_MODEL = "dbmdz/bert-large-cased-finetuned-conll03-english"
ALTERNATIVE_MODELS = [
    "microsoft/DialoGPT-medium",
    "bert-base-uncased",
    "distilbert-base-uncased"
]

# NER Configuration
NER_CONFIDENCE_THRESHOLD = 0.7
NER_ENTITY_TYPES = [
    "PERSON", "ORG", "GPE", "DATE", "TIME", "MONEY", "PERCENT", "QUANTITY"
]

# Pattern Configuration
REQUIREMENT_PATTERNS = [
    # Experience patterns
    r'\b\d+\+?\s*years?\s*of?\s*experience\b',
    r'\b(?:senior|junior|entry|mid|senior)\s*level\b',
    
    # Education patterns
    r'\b(?:bachelor|master|phd|degree)\s*in\b',
    r'\b(?:certification|certified)\b',
    r'\b(?:diploma|associate)\s*degree\b',
    
    # Skill patterns
    r'\b(?:proficient|expert|skilled|experienced)\s*in\b',
    r'\b(?:knowledge|understanding|familiarity)\s*of\b',
    r'\b(?:experience|background)\s*with\b',
    
    # Requirement keywords
    r'\b(?:required|must|should|preferred|desired)\b',
    r'\b(?:essential|necessary|mandatory)\b',
    
    # Technical skills
    r'\b(?:python|java|javascript|typescript|react|angular|vue)\b',
    r'\b(?:sql|mysql|postgresql|mongodb|redis)\b',
    r'\b(?:aws|azure|gcp|docker|kubernetes|terraform)\b',
    r'\b(?:git|jenkins|jira|confluence|slack|teams)\b',
    
    # Methodologies
    r'\b(?:agile|scrum|waterfall|kanban|lean)\b',
    r'\b(?:ci/cd|devops|mlops|dataops)\b',
    
    # Soft skills
    r'\b(?:leadership|management|communication)\s*skills\b',
    r'\b(?:teamwork|collaboration|problem-solving)\s*skills\b',
    r'\b(?:analytical|critical\s*thinking)\s*skills\b'
]

# Category Configuration
REQUIREMENT_CATEGORIES = {
    'experience': [
        'years', 'experience', 'senior', 'junior', 'entry', 'mid', 'level',
        'background', 'track record', 'proven'
    ],
    'education': [
        'degree', 'bachelor', 'master', 'phd', 'certification', 'diploma',
        'associate', 'qualification', 'academic'
    ],
    'technical_skills': [
        'python', 'java', 'javascript', 'typescript', 'react', 'angular',
        'vue', 'node', 'sql', 'aws', 'azure', 'gcp', 'docker', 'kubernetes'
    ],
    'soft_skills': [
        'communication', 'leadership', 'teamwork', 'problem-solving',
        'analytical', 'critical thinking', 'collaboration', 'interpersonal'
    ],
    'tools': [
        'git', 'jenkins', 'jira', 'confluence', 'slack', 'teams',
        'trello', 'asana', 'notion', 'figma'
    ],
    'methodologies': [
        'agile', 'scrum', 'waterfall', 'kanban', 'lean', 'ci/cd',
        'devops', 'mlops', 'dataops', 'tdd', 'bdd'
    ],
    'languages': [
        'english', 'spanish', 'french', 'german', 'chinese', 'japanese',
        'korean', 'russian', 'arabic', 'hindi'
    ],
    'industries': [
        'finance', 'healthcare', 'e-commerce', 'education', 'technology',
        'manufacturing', 'retail', 'consulting', 'government'
    ]
}

# Text Processing Configuration
MIN_SENTENCE_LENGTH = 10
MAX_SENTENCE_LENGTH = 500
MIN_WORD_LENGTH = 2
MAX_WORD_LENGTH = 50

# Complexity Scoring Configuration
COMPLEXITY_WEIGHTS = {
    'avg_word_length': 0.3,
    'avg_sentence_length': 0.4,
    'technical_density': 0.3
}

TECHNICAL_TERMS = [
    'api', 'database', 'algorithm', 'framework', 'architecture',
    'deployment', 'infrastructure', 'microservices', 'kubernetes',
    'docker', 'terraform', 'jenkins', 'gitlab', 'jira'
]

# Output Configuration
MAX_REQUIREMENTS_DISPLAY = 10
MAX_CATEGORY_ITEMS = 5
JSON_INDENT = 2

# Web Interface Configuration
STREAMLIT_CONFIG = {
    'page_title': "Job Requirements Extractor",
    'page_icon': "💼",
    'layout': "wide",
    'initial_sidebar_state': "expanded"
}

# File Upload Configuration
ALLOWED_FILE_TYPES = ['.txt', '.md', '.docx']
MAX_FILE_SIZE_MB = 10

# Performance Configuration
BATCH_SIZE = 32
MAX_TEXT_LENGTH = 10000
CACHE_MODELS = True

# Logging Configuration
LOG_LEVEL = "INFO"
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

# Environment Variables
def get_env_config() -> Dict[str, Any]:
    """Get configuration from environment variables."""
    return {
        'model_name': os.getenv('JRE_MODEL_NAME', DEFAULT_MODEL),
        'confidence_threshold': float(os.getenv('JRE_CONFIDENCE', NER_CONFIDENCE_THRESHOLD)),
        'log_level': os.getenv('JRE_LOG_LEVEL', LOG_LEVEL),
        'cache_models': os.getenv('JRE_CACHE_MODELS', 'true').lower() == 'true',
        'max_text_length': int(os.getenv('JRE_MAX_TEXT_LENGTH', MAX_TEXT_LENGTH)),
        'batch_size': int(os.getenv('JRE_BATCH_SIZE', BATCH_SIZE))
    }

# Validation Configuration
def validate_config() -> bool:
    """Validate configuration settings."""
    try:
        # Check if confidence threshold is valid
        if not 0.0 <= NER_CONFIDENCE_THRESHOLD <= 1.0:
            raise ValueError("NER confidence threshold must be between 0.0 and 1.0")
        
        # Check if complexity weights sum to 1.0
        weight_sum = sum(COMPLEXITY_WEIGHTS.values())
        if abs(weight_sum - 1.0) > 0.001:
            raise ValueError(f"Complexity weights must sum to 1.0, got {weight_sum}")
        
        # Check if patterns are valid regex
        import re
        for pattern in REQUIREMENT_PATTERNS:
            re.compile(pattern)
        
        return True
        
    except Exception as e:
        print(f"Configuration validation failed: {e}")
        return False

if __name__ == "__main__":
    # Test configuration
    if validate_config():
        print("✅ Configuration validation passed")
        
        env_config = get_env_config()
        print(f"📋 Environment configuration: {env_config}")
        
        print(f"🔧 Default model: {DEFAULT_MODEL}")
        print(f"🎯 Confidence threshold: {NER_CONFIDENCE_THRESHOLD}")
        print(f"🏷️  Categories: {len(REQUIREMENT_CATEGORIES)}")
        print(f"🔍 Patterns: {len(REQUIREMENT_PATTERNS)}")
        
    else:
        print("❌ Configuration validation failed")
        exit(1)
