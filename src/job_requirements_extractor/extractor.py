import re
import json
from typing import List, Dict, Any
from transformers import pipeline, AutoTokenizer, AutoModelForTokenClassification
import torch
from sentence_transformers import SentenceTransformer
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

class JobRequirementsExtractor:
    def __init__(self, model_name: str = "microsoft/DialoGPT-medium"):
        """
        Initialize the job requirements extractor with a Hugging Face model.
        
        Args:
            model_name: Name of the Hugging Face model to use
        """
        self.model_name = model_name
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        
        # Initialize the NER pipeline for extracting entities
        try:
            self.ner_pipeline = pipeline(
                "ner",
                model="dbmdz/bert-large-cased-finetuned-conll03-english",
                device=0 if self.device == "cuda" else -1
            )
        except Exception as e:
            # Silently continue if NER model fails to load
            self.ner_pipeline = None
        
        # Initialize sentence transformer for similarity matching
        try:
            self.sentence_transformer = SentenceTransformer('all-MiniLM-L6-v2')
        except Exception as e:
            # Silently continue if sentence transformer fails to load
            self.sentence_transformer = None
        
        # Common job requirement patterns
        self.requirement_patterns = [
            r'\b\d+\+?\s*years?\s*of?\s*experience\b',
            r'\b(?:bachelor|master|phd|degree)\s*in\b',
            r'\b(?:proficient|expert|skilled|experienced)\s*in\b',
            r'\b(?:knowledge|understanding|familiarity)\s*of\b',
            r'\b(?:certification|certified)\b',
            r'\b(?:required|must|should|preferred)\b',
            r'\b(?:python|java|javascript|sql|aws|docker|kubernetes)\b',
            r'\b(?:agile|scrum|waterfall)\b',
            r'\b(?:leadership|management|communication)\s*skills\b'
        ]
        
        # Common requirement categories
        self.categories = {
            'experience': ['years', 'experience', 'senior', 'junior', 'entry'],
            'education': ['degree', 'bachelor', 'master', 'phd', 'certification'],
            'technical_skills': ['python', 'java', 'javascript', 'sql', 'aws', 'docker'],
            'soft_skills': ['communication', 'leadership', 'teamwork', 'problem-solving'],
            'tools': ['git', 'jira', 'confluence', 'slack', 'teams'],
            'methodologies': ['agile', 'scrum', 'waterfall', 'kanban']
        }

    def extract_requirements(self, job_description: str) -> Dict[str, Any]:
        """
        Extract requirements from a job description.
        
        Args:
            job_description: The job description text
            
        Returns:
            Dictionary containing extracted requirements organized by category
        """
        if not job_description:
            return {"error": "No job description provided"}
        
        # Clean the text for text-based extraction
        cleaned_text = self._clean_text(job_description)
        
        # Extract individual requirements from ORIGINAL text (before cleaning)
        individual_reqs = self._extract_individual_requirements(job_description)
        
        # Extract requirements using different methods
        requirements = {
            'text_requirements': self._extract_text_patterns(cleaned_text),
            'individual_requirements': individual_reqs,
            'entity_requirements': self._extract_entities(cleaned_text),
            'categorized_requirements': self._categorize_requirements(job_description),  # Use original text for categorization
            'summary': self._generate_summary(job_description)  # Use original text for summary
        }
        
        return requirements

    def _clean_text(self, text: str) -> str:
        """Clean and preprocess the text."""
        # Remove extra whitespace but preserve newlines for bullet point detection
        text = re.sub(r'[ \t]+', ' ', text)  # Only collapse spaces and tabs, not newlines
        # Remove special characters but keep important ones including bullet points
        text = re.sub(r'[^\w\s\-\.\,\;\:\!\?\(\)•\-\*]', '', text)
        return text.strip()

    def _extract_text_patterns(self, text: str) -> List[str]:
        """Extract requirements using full sentences containing requirement keywords."""
        requirements = []
        
        # Split text into sentences and bullet points (more robust splitting)
        # Handle various sentence endings, bullet points, and numbered lists
        sentences = re.split(r'[.!?]+|\n-|\n•|\n\*|\n\d+\.|\n\d+\)', text)
        
        # Define requirement keywords that indicate a sentence contains requirements
        requirement_keywords = [
            'required', 'must', 'should', 'preferred', 'desired', 'essential',
            'necessary', 'mandatory', 'experience', 'skills', 'knowledge',
            'proficient', 'expert', 'skilled', 'qualified', 'background',
            'understanding', 'familiarity', 'certification', 'degree',
            'years', 'senior', 'junior', 'entry', 'level'
        ]
        
        for sentence in sentences:
            sentence = sentence.strip()
            
            # Skip very short sentences and empty ones
            if len(sentence) < 10:
                continue
                
            # Check if sentence contains requirement-related content
            sentence_lower = sentence.lower()
            
            # Look for requirement keywords in the sentence
            if any(keyword in sentence_lower for keyword in requirement_keywords):
                # Additional filtering to ensure it's actually a requirement
                # Skip sentences that are just general descriptions
                skip_indicators = [
                    'we offer', 'we provide', 'benefits include', 'responsibilities',
                    'duties', 'about us', 'company', 'team', 'culture'
                ]
                
                if not any(skip in sentence_lower for skip in skip_indicators):
                    requirements.append(sentence)
        
        # Clean and format the requirements
        cleaned_requirements = []
        for req in requirements:
            # Clean up the sentence
            cleaned = req.strip()
            # Remove leading bullet points, dashes, or numbers
            cleaned = re.sub(r'^[-•\*\s\d\.\)]+', '', cleaned)
            # Ensure proper capitalization
            if cleaned and len(cleaned) > 0:
                cleaned = cleaned[0].upper() + cleaned[1:] if cleaned[0].isalpha() else cleaned
                cleaned_requirements.append(cleaned)
        
        # Remove duplicates and return
        return list(set(cleaned_requirements))

    def _extract_individual_requirements(self, text: str) -> List[str]:
        """Extract individual requirements from bullet points and lists."""
        individual_reqs = []
        
        # Split by common list indicators
        lines = text.split('\n')
        
        for line in lines:
            # Skip empty lines (check before stripping)
            if not line.strip():
                continue
                
            # Check if line starts with bullet points, dashes, numbers, OR is indented
            # More flexible pattern matching including indented lines
            is_bullet_point = re.match(r'^[\s]*[-•\*\s\d\.\)]+[\s]*', line)
            is_indented = re.match(r'^[\s]{4,}', line)  # Lines with 4+ spaces (indented)
            
            if is_bullet_point or is_indented:
                # Clean the line
                if is_bullet_point:
                    cleaned = re.sub(r'^[\s]*[-•\*\s\d\.\)]+[\s]*', '', line).strip()
                else:
                    cleaned = line.strip()
                
                # Check if it contains requirement-related content
                if len(cleaned) > 3:  # Lower threshold for all list items
                    line_lower = cleaned.lower()
                    requirement_indicators = [
                        # Basic requirement keywords
                        'required', 'must', 'should', 'preferred', 'desired', 'essential',
                        'necessary', 'mandatory', 'experience', 'skills', 'knowledge',
                        'proficient', 'expert', 'skilled', 'qualified', 'background',
                        'understanding', 'familiarity', 'certification', 'degree',
                        'years', 'senior', 'junior', 'entry', 'level',
                        
                        # Technical skills
                        'python', 'java', 'javascript', 'aws', 'docker', 'kubernetes', 
                        'sql', 'agile', 'git', 'ci/cd', 'api', 'machine learning', 
                        'tensorflow', 'pytorch', 'microservices', 'monitoring', 'security',
                        'net', 'c#', 'asp.net', 'html', 'css', 'angular', 'ionic',
                        
                        # Management and leadership keywords
                        'lead', 'mentor', 'manage', 'team', 'leadership', 'management',
                        'foster', 'culture', 'conduct', 'reviews', 'planning', 'delivery',
                        'oversee', 'drive', 'ensure', 'maintain', 'champion', 'collaborate',
                        'liaise', 'translate', 'requirements', 'solutions', 'stakeholders',
                        'timelines', 'sprint', 'resource', 'allocation', 'progress',
                        'reporting', 'quality', 'operations', 'reliability', 'performance',
                        'security', 'production', 'improvement', 'innovation', 'processes'
                    ]
                    
                    # Check if line contains any requirement indicators
                    if any(indicator in line_lower for indicator in requirement_indicators):
                        # Ensure proper capitalization
                        if cleaned and len(cleaned) > 0:
                            cleaned = cleaned[0].upper() + cleaned[1:] if cleaned[0].isalpha() else cleaned
                            individual_reqs.append(cleaned)
        
        return individual_reqs

    def _extract_entities(self, text: str) -> List[Dict[str, Any]]:
        """Extract named entities using the NER pipeline."""
        if not self.ner_pipeline:
            return []
        
        try:
            entities = self.ner_pipeline(text)
            
            # Filter for relevant entities
            relevant_entities = []
            for entity in entities:
                try:
                    # Ensure entity has required fields
                    if not isinstance(entity, dict):
                        continue
                    
                    # Handle both old and new entity formats
                    entity_type = entity.get('entity_group') or entity.get('entity_type') or 'UNKNOWN'
                    entity_text = entity.get('word') or entity.get('text') or str(entity)
                    entity_score = entity.get('score') or 0.0
                    
                    if entity_score > 0.7:  # Only high-confidence entities
                        relevant_entities.append({
                            'text': entity_text,
                            'type': entity_type,
                            'confidence': entity_score
                        })
                except Exception as entity_error:
                    # Silently continue on entity processing errors
                    continue
            
            return relevant_entities
        except Exception as e:
            # Return empty list on any extraction errors
            return []

    def _categorize_requirements(self, text: str) -> Dict[str, List[str]]:
        """Categorize requirements into different types."""
        categorized = {category: [] for category in self.categories.keys()}
        
        # First, extract individual requirements for better categorization
        individual_reqs = self._extract_individual_requirements(text)
        
        # Also get text-based requirements
        text_reqs = self._extract_text_patterns(text)
        
        # Combine all requirements for categorization
        all_requirements = individual_reqs + text_reqs
        
        for req in all_requirements:
            if not req or len(req) < 10:
                continue
                
            req_lower = req.lower()
            
            # Categorize based on content
            for category, keywords in self.categories.items():
                if any(keyword in req_lower for keyword in keywords):
                    # Clean and format the requirement
                    cleaned = req.strip()
                    cleaned = re.sub(r'^[-•\*\s\d\.\)]+', '', cleaned)
                    if cleaned and len(cleaned) > 0:
                        cleaned = cleaned[0].upper() + cleaned[1:] if cleaned[0].isalpha() else cleaned
                        # Avoid duplicates
                        if cleaned not in categorized[category]:
                            categorized[category].append(cleaned)
        
        # Remove empty categories
        return {k: v for k, v in categorized.items() if v}

    def _generate_summary(self, text: str) -> Dict[str, Any]:
        """Generate a summary of the requirements."""
        # Split into sentences using the same method as requirement extraction
        sentences = re.split(r'[.!?]+|\n-|\n•|\n\*', text)
        sentences = [s.strip() for s in sentences if len(s.strip()) > 20]
        
        # Count requirement-related keywords
        requirement_keywords = [
            'required', 'must', 'should', 'preferred', 'desired', 'essential',
            'necessary', 'mandatory', 'experience', 'skills', 'knowledge',
            'proficient', 'expert', 'skilled', 'qualified', 'background',
            'understanding', 'familiarity', 'certification', 'degree',
            'years', 'senior', 'junior', 'entry', 'level'
        ]
        requirement_count = sum(1 for sentence in sentences 
                              if any(keyword in sentence.lower() for keyword in requirement_keywords))
        
        # Get the actual extracted requirements count
        extracted_requirements = self._extract_text_patterns(text)
        individual_requirements = self._extract_individual_requirements(text)
        
        return {
            'total_sentences': len(sentences),
            'requirement_sentences': requirement_count,
            'requirement_density': requirement_count / len(sentences) if sentences else 0,
            'estimated_requirements': len(extracted_requirements) + len(individual_requirements)
        }

    def analyze_job_description(self, job_description: str) -> Dict[str, Any]:
        """
        Comprehensive analysis of a job description.
        
        Args:
            job_description: The job description text
            
        Returns:
            Dictionary containing comprehensive analysis
        """
        requirements = self.extract_requirements(job_description)
        
        # Add additional analysis
        analysis = {
            'requirements': requirements,
            'text_length': len(job_description),
            'word_count': len(job_description.split()),
            'complexity_score': self._calculate_complexity(job_description),
            'recommendations': self._generate_recommendations(requirements)
        }
        
        return analysis

    def _calculate_complexity(self, text: str) -> float:
        """Calculate a complexity score for the job description."""
        words = text.split()
        if not words:
            return 0.0
        
        # Average word length
        avg_word_length = sum(len(word) for word in words) / len(words)
        
        # Sentence complexity (longer sentences = more complex)
        sentences = re.split(r'[.!?]+', text)
        avg_sentence_length = sum(len(s.split()) for s in sentences if s.strip()) / len(sentences) if sentences else 0
        
        # Technical term density
        technical_terms = ['api', 'database', 'algorithm', 'framework', 'architecture', 'deployment', 'infrastructure']
        technical_count = sum(1 for word in words if word.lower() in technical_terms)
        technical_density = technical_count / len(words)
        
        # Normalize scores
        complexity = (avg_word_length * 0.3 + avg_sentence_length * 0.4 + technical_density * 0.3)
        return min(complexity, 10.0)  # Cap at 10

    def _generate_recommendations(self, requirements: Dict[str, Any]) -> List[str]:
        """Generate recommendations based on extracted requirements."""
        recommendations = []
        
        if requirements.get('categorized_requirements'):
            cats = requirements['categorized_requirements']
            
            if 'technical_skills' in cats and len(cats['technical_skills']) > 0:
                recommendations.append("Focus on highlighting relevant technical skills in your resume")
            
            if 'experience' in cats and len(cats['experience']) > 0:
                recommendations.append("Emphasize relevant work experience and achievements")
            
            if 'education' in cats and len(cats['education']) > 0:
                recommendations.append("Ensure your education credentials are clearly stated")
        
        if requirements.get('summary', {}).get('requirement_density', 0) > 0.3:
            recommendations.append("This job has many requirements - consider if you meet most criteria")
        else:
            recommendations.append("This job has fewer requirements - may be more entry-level")
        
        return recommendations
