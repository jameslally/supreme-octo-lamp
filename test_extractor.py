#!/usr/bin/env python3
"""
Simple test script to demonstrate the Job Requirements Extractor
"""

from job_requirements_extractor import JobRequirementsExtractor

def test_basic_extraction():
    """Test basic requirement extraction functionality."""
    
    # Sample job descriptions for testing
    test_jobs = [
        {
            "title": "Junior Python Developer",
            "description": """
            We are seeking a Junior Python Developer to join our team.
            Requirements:
            - Basic knowledge of Python programming
            - Understanding of web development concepts
            - Bachelor's degree in Computer Science or related field
            - 0-2 years of experience
            - Good communication skills
            """
        },
        {
            "title": "Senior Data Scientist",
            "description": """
            Senior Data Scientist Position
            
            We need an experienced data scientist with:
            - 5+ years of experience in machine learning
            - PhD or Master's degree in Statistics, Mathematics, or Computer Science
            - Proficiency in Python, R, and SQL
            - Experience with TensorFlow, PyTorch, and scikit-learn
            - Knowledge of AWS cloud services
            - Experience with big data technologies (Spark, Hadoop)
            - Strong analytical and problem-solving skills
            - Leadership experience in technical teams
            """
        },
        {
            "title": "DevOps Engineer",
            "description": """
            DevOps Engineer
            
            Required Skills:
            - 3+ years of DevOps experience
            - Experience with Docker and Kubernetes
            - Knowledge of CI/CD pipelines
            - Familiarity with AWS, Azure, or GCP
            - Experience with monitoring tools (Prometheus, Grafana)
            - Knowledge of infrastructure as code (Terraform, CloudFormation)
            - Experience with Git and version control
            - Strong scripting skills (Python, Bash)
            """
        }
    ]
    
    print("🚀 Testing Job Requirements Extractor")
    print("=" * 50)
    
    # Initialize the extractor
    extractor = JobRequirementsExtractor()
    
    for i, job in enumerate(test_jobs, 1):
        print(f"\n📋 Test Case {i}: {job['title']}")
        print("-" * 40)
        
        try:
            # Extract requirements
            analysis = extractor.analyze_job_description(job['description'])
            
            # Display key results
            requirements = analysis.get('requirements', {})
            
            print(f"📊 Complexity Score: {analysis.get('complexity_score', 0):.1f}/10")
            print(f"📝 Word Count: {analysis.get('word_count', 0)}")
            
            if 'summary' in requirements:
                summary = requirements['summary']
                print(f"🔍 Requirements Found: {summary.get('estimated_requirements', 0)}")
                print(f"📈 Requirement Density: {summary.get('requirement_density', 0):.1%}")
            
            # Show categorized requirements
            if 'categorized_requirements' in requirements:
                cats = requirements['categorized_requirements']
                print("\n🏷️  Categories Found:")
                for category, items in cats.items():
                    if items:
                        print(f"   {category.replace('_', ' ').title()}: {len(items)} items")
            
            # Show top text requirements
            if 'text_requirements' in requirements and requirements['text_requirements']:
                print(f"\n🔍 Top Requirements:")
                for j, req in enumerate(requirements['text_requirements'][:3], 1):
                    print(f"   {j}. {req[:80]}{'...' if len(req) > 80 else ''}")
            
            print("✅ Analysis completed successfully!")
            
        except Exception as e:
            print(f"❌ Error during analysis: {e}")
        
        print()

def test_specific_patterns():
    """Test specific requirement pattern extraction."""
    
    print("🧪 Testing Specific Pattern Extraction")
    print("=" * 50)
    
    extractor = JobRequirementsExtractor()
    
    # Test specific patterns
    test_patterns = [
        "We need someone with 5+ years of experience",
        "Bachelor's degree in Computer Science required",
        "Must be proficient in Python and JavaScript",
        "Experience with AWS cloud services preferred",
        "Strong communication and leadership skills needed"
    ]
    
    for pattern in test_patterns:
        print(f"\n🔍 Testing: {pattern}")
        try:
            analysis = extractor.extract_requirements(pattern)
            if 'text_requirements' in analysis and analysis['text_requirements']:
                print(f"   ✅ Found: {analysis['text_requirements'][0]}")
            else:
                print("   ❌ No requirements found")
        except Exception as e:
            print(f"   ❌ Error: {e}")

if __name__ == "__main__":
    print("🎯 Job Requirements Extractor - Test Suite")
    print("=" * 60)
    
    try:
        # Run basic tests
        test_basic_extraction()
        
        # Run pattern tests
        test_specific_patterns()
        
        print("\n🎉 All tests completed!")
        print("\n💡 To run the full application:")
        print("   Web Interface: streamlit run app.py")
        print("   Command Line: python cli.py -t 'your job description'")
        
    except Exception as e:
        print(f"\n❌ Test suite failed: {e}")
        print("Please check your installation and dependencies.")
