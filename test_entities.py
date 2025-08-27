#!/usr/bin/env python3
"""
Simple test script to verify entity extraction works without PowerShell errors.
"""

import sys
import os
from pathlib import Path

def test_entity_extraction():
    """Test entity extraction without problematic output."""
    print("🧪 Testing Entity Extraction...")
    
    # Add src to Python path
    project_root = Path(__file__).parent.absolute()
    src_path = str(project_root / "src")
    if src_path not in sys.path:
        sys.path.insert(0, src_path)
    
    try:
        from job_requirements_extractor import JobRequirementsExtractor
        
        print("✅ Successfully imported JobRequirementsExtractor")
        
        # Create an instance
        extractor = JobRequirementsExtractor()
        
        if extractor.ner_pipeline is None:
            print("ℹ️  NER pipeline not loaded (this is normal if dependencies aren't installed)")
            print("✅ Entity extraction will return empty list (no errors)")
            return True
        
        print("✅ NER pipeline loaded successfully")
        
        # Test text
        test_text = "We are looking for a Python developer with 5+ years of experience in machine learning and AWS."
        
        print(f"📝 Testing with: {test_text}")
        
        # Test entity extraction
        try:
            entities = extractor._extract_entities(test_text)
            print(f"✅ Entity extraction successful: {len(entities)} entities found")
            
            if entities:
                print("📊 Sample entities:")
                for i, entity in enumerate(entities[:3]):  # Show first 3
                    print(f"   {i+1}. {entity['text']} ({entity['type']}) - Confidence: {entity['confidence']:.2f}")
            
            return True
            
        except Exception as e:
            print(f"❌ Entity extraction failed: {e}")
            return False
            
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("💡 Try installing the package: pip install -e .")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False

if __name__ == "__main__":
    success = test_entity_extraction()
    if success:
        print("\n🎉 Entity extraction test completed successfully!")
    else:
        print("\n💥 Entity extraction test failed!")
        sys.exit(1)
