#!/usr/bin/env python3
"""
Debug script to troubleshoot entity extraction issues.
"""

import sys
import os
from pathlib import Path

def debug_entity_extraction():
    """Debug the entity extraction process."""
    print("🔍 Debugging Entity Extraction...")
    
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
            print("❌ NER pipeline is None - model failed to load")
            return
        
        print(f"✅ NER pipeline loaded: {type(extractor.ner_pipeline)}")
        
        # Test text
        test_text = "We are looking for a Python developer with 5+ years of experience in machine learning and AWS."
        
        print(f"\n📝 Test text: {test_text}")
        
        # Test the NER pipeline directly
        print("\n🔍 Testing NER pipeline directly...")
        try:
            entities = extractor.ner_pipeline(test_text)
            print(f"✅ NER pipeline returned {len(entities)} entities")
            
            if entities:
                print(f"\n📊 First entity structure:")
                print(f"   Type: {type(entities[0])}")
                print(f"   Content: {entities[0]}")
                
                if isinstance(entities[0], dict):
                    print(f"   Keys: {list(entities[0].keys())}")
                    
                    # Check for entity_group vs entity_type
                    if 'entity_group' in entities[0]:
                        print("   ✅ Found 'entity_group' key")
                    if 'entity_type' in entities[0]:
                        print("   ✅ Found 'entity_type' key")
                    if 'word' in entities[0]:
                        print("   ✅ Found 'word' key")
                    if 'text' in entities[0]:
                        print("   ✅ Found 'text' key")
                    if 'score' in entities[0]:
                        print("   ✅ Found 'score' key")
                
        except Exception as e:
            print(f"❌ Error testing NER pipeline: {e}")
            import traceback
            traceback.print_exc()
        
        # Test the extractor's entity extraction method
        print("\n🔍 Testing extractor's entity extraction method...")
        try:
            entity_results = extractor._extract_entities(test_text)
            print(f"✅ Extractor returned {len(entity_results)} entities")
            
            if entity_results:
                print(f"\n📊 First extracted entity:")
                print(f"   {entity_results[0]}")
                
        except Exception as e:
            print(f"❌ Error in extractor entity extraction: {e}")
            import traceback
            traceback.print_exc()
        
        # Test the full requirements extraction
        print("\n🔍 Testing full requirements extraction...")
        try:
            requirements = extractor.extract_requirements(test_text)
            print(f"✅ Full extraction successful")
            print(f"   Entity requirements: {len(requirements.get('entity_requirements', []))}")
            
        except Exception as e:
            print(f"❌ Error in full extraction: {e}")
            import traceback
            traceback.print_exc()
            
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("💡 Try installing the package: pip install -e .")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    debug_entity_extraction()
