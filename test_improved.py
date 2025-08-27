#!/usr/bin/env python3
"""
Test script for the improved job requirements extractor
"""

from job_requirements_extractor import JobRequirementsExtractor

def test_improved_extractor():
    # Read the example job file
    with open('example_job2.txt', 'r', encoding='utf-8') as f:
        job_description = f.read()

    # Initialize the extractor
    extractor = JobRequirementsExtractor()

    # Analyze the job description
    analysis = extractor.analyze_job_description(job_description)

    # Print results
    print('=== IMPROVED EXTRACTOR TEST ===')
    print('Individual Requirements Found:', len(analysis['requirements']['individual_requirements']))
    print('Text Requirements Found:', len(analysis['requirements']['text_requirements']))
    print('Total Estimated Requirements:', analysis['requirements']['summary']['estimated_requirements'])

    print('\n🔹 Individual Requirements:')
    for i, req in enumerate(analysis['requirements']['individual_requirements'][:15], 1):
        print(f'{i}. {req}')

    print('\n🏷️ Categorized Requirements:')
    for category, items in analysis['requirements']['categorized_requirements'].items():
        if items:
            print(f'\n{category.replace("_", " ").title()}:')
            for item in items[:3]:
                print(f'  - {item}')

if __name__ == "__main__":
    test_improved_extractor()
