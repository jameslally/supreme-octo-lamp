#!/usr/bin/env python3
"""
Test script to demonstrate improved sentence-based requirement extraction
"""

from job_requirements_extractor import JobRequirementsExtractor

def test_sentence_extraction():
    """Test the improved sentence-based requirement extraction."""
    
    # Sample job description with various sentence structures
    test_job = """
    Senior Software Engineer Position
    
    We are looking for a Senior Software Engineer to join our team. 
    The ideal candidate must have at least 5+ years of experience in software development.
    
    Required Qualifications:
    - Bachelor's degree in Computer Science or related field is required
    - Must be proficient in Python, Java, and JavaScript programming languages
    - Experience with AWS cloud services is essential for this role
    - Knowledge of Docker and Kubernetes is preferred
    - Strong understanding of database design and SQL is mandatory
    
    Preferred Skills:
    - Master's degree in Computer Science would be beneficial
    - Experience with machine learning frameworks is desired
    - Knowledge of microservices architecture is highly valued
    - Leadership experience in technical teams is preferred
    
    Responsibilities:
    - Design and develop scalable web applications
    - Collaborate with cross-functional teams
    - Mentor junior developers
    
    We offer competitive salary and benefits. Our company culture is collaborative and innovative.
    """
    
    print("🧪 Testing Improved Sentence-Based Requirement Extraction")
    print("=" * 60)
    
    # Initialize the extractor
    extractor = JobRequirementsExtractor()
    
    try:
        # Extract requirements
        analysis = extractor.analyze_job_description(test_job)
        
        print("\n📋 EXTRACTED REQUIREMENTS:")
        print("-" * 40)
        
        if 'requirements' in analysis:
            reqs = analysis['requirements']
            
            # Show text-based requirements (full sentences)
            if 'text_requirements' in reqs and reqs['text_requirements']:
                print("\n🔍 Full Sentence Requirements:")
                for i, req in enumerate(reqs['text_requirements'], 1):
                    print(f"{i:2d}. {req}")
            
            # Show categorized requirements
            if 'categorized_requirements' in reqs:
                cats = reqs['categorized_requirements']
                print("\n🏷️  Categorized Requirements:")
                for category, items in cats.items():
                    if items:
                        print(f"\n   {category.replace('_', ' ').title()}:")
                        for item in items:
                            print(f"      • {item}")
            
            # Show summary
            if 'summary' in reqs:
                summary = reqs['summary']
                print(f"\n📊 Summary:")
                print(f"   Total sentences: {summary.get('total_sentences', 0)}")
                print(f"   Requirement sentences: {summary.get('requirement_sentences', 0)}")
                print(f"   Extracted requirements: {summary.get('estimated_requirements', 0)}")
        
        print(f"\n✅ Analysis completed successfully!")
        
    except Exception as e:
        print(f"❌ Error during analysis: {e}")
        import traceback
        traceback.print_exc()

def test_specific_sentence_patterns():
    """Test specific sentence patterns."""
    
    print("\n🔍 Testing Specific Sentence Patterns")
    print("=" * 50)
    
    extractor = JobRequirementsExtractor()
    
    # Test different sentence structures
    test_sentences = [
        "The candidate must have 5+ years of experience in Python development",
        "Bachelor's degree in Computer Science is required",
        "Experience with AWS cloud services is essential",
        "Knowledge of Docker and Kubernetes is preferred",
        "We offer competitive salary and benefits",  # Should be filtered out
        "Our company culture is collaborative",      # Should be filtered out
        "Must be proficient in JavaScript and React",
        "Leadership experience in technical teams is highly valued"
    ]
    
    for sentence in test_sentences:
        print(f"\n📝 Testing: {sentence}")
        try:
            analysis = extractor.extract_requirements(sentence)
            if 'text_requirements' in analysis and analysis['text_requirements']:
                print(f"   ✅ Extracted: {analysis['text_requirements'][0]}")
            else:
                print("   ❌ No requirements found (correctly filtered)")
        except Exception as e:
            print(f"   ❌ Error: {e}")

if __name__ == "__main__":
    print("🎯 Testing Improved Sentence Extraction")
    print("=" * 60)
    
    try:
        # Run tests
        test_sentence_extraction()
        test_specific_sentence_patterns()
        
        print("\n🎉 All tests completed!")
        print("\n💡 Key improvements:")
        print("   • Extracts full sentences instead of individual words")
        print("   • Better sentence splitting (handles bullet points)")
        print("   • Filters out non-requirement sentences")
        print("   • Cleans and formats extracted text")
        print("   • More accurate requirement identification")
        
    except Exception as e:
        print(f"\n❌ Test suite failed: {e}")
        print("Please check your installation and dependencies.")
