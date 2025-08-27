"""
Job Requirements Extractor Package

A comprehensive tool for extracting and analyzing requirements from job descriptions
using advanced NLP techniques including Named Entity Recognition and pattern matching.
"""

from .extractor import JobRequirementsExtractor
from .batch_processor import BatchJobProcessor
from .config import (
    DEFAULT_MODEL,
    NER_CONFIDENCE_THRESHOLD,
    REQUIREMENT_PATTERNS,
    REQUIREMENT_CATEGORIES,
    get_env_config,
    validate_config
)

__version__ = "1.0.0"
__author__ = "Job Requirements Extractor Team"

__all__ = [
    "JobRequirementsExtractor",
    "BatchJobProcessor",
    "DEFAULT_MODEL",
    "NER_CONFIDENCE_THRESHOLD",
    "REQUIREMENT_PATTERNS",
    "REQUIREMENT_CATEGORIES",
    "get_env_config",
    "validate_config"
]
