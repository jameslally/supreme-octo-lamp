#!/usr/bin/env python3
"""
Command Line Interface for Job Requirements Extractor
"""

import argparse
import sys
import json
from pathlib import Path
from job_requirements_extractor import JobRequirementsExtractor

def read_file(file_path: str) -> str:
    """Read content from a file."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        print(f"Error reading file {file_path}: {e}")
        sys.exit(1)

def save_results(results: dict, output_file: str):
    """Save results to a JSON file."""
    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2, default=str)
        print(f"Results saved to {output_file}")
    except Exception as e:
        print(f"Error saving results: {e}")

def print_results(analysis: dict, verbose: bool = False):
    """Print analysis results in a formatted way."""
    print("\n" + "="*60)
    print("🎯 JOB REQUIREMENTS ANALYSIS RESULTS")
    print("="*60)
    
    # Basic metrics
    print(f"\n📊 BASIC METRICS:")
    print(f"   Text Length: {analysis.get('text_length', 0):,} characters")
    print(f"   Word Count: {analysis.get('word_count', 0):,} words")
    print(f"   Complexity Score: {analysis.get('complexity_score', 0):.1f}/10")
    
    requirements = analysis.get('requirements', {})
    
    # Requirements summary
    if 'summary' in requirements:
        summary = requirements['summary']
        print(f"\n📋 REQUIREMENTS SUMMARY:")
        print(f"   Total Sentences: {summary.get('total_sentences', 0)}")
        print(f"   Requirement Sentences: {summary.get('requirement_sentences', 0)}")
        print(f"   Estimated Requirements: {summary.get('estimated_requirements', 0)}")
        print(f"   Requirement Density: {summary.get('requirement_density', 0):.1%}")
    
    # Text-based requirements
    if 'text_requirements' in requirements and requirements['text_requirements']:
        print(f"\n🔍 PATTERN-BASED REQUIREMENTS:")
        for i, req in enumerate(requirements['text_requirements'][:10], 1):
            print(f"   {i:2d}. {req}")
        
        if len(requirements['text_requirements']) > 10:
            print(f"   ... and {len(requirements['text_requirements']) - 10} more")
    
    # Categorized requirements
    if 'categorized_requirements' in requirements and requirements['categorized_requirements']:
        print(f"\n🏷️  CATEGORIZED REQUIREMENTS:")
        cats = requirements['categorized_requirements']
        
        for category, items in cats.items():
            if items:
                print(f"\n   {category.replace('_', ' ').upper()}:")
                for item in items[:5]:  # Show first 5 items
                    display_item = item[:80] + "..." if len(item) > 80 else item
                    print(f"      • {display_item}")
                
                if len(items) > 5:
                    print(f"      ... and {len(items) - 5} more")
    
    # Recommendations
    if 'recommendations' in analysis and analysis['recommendations']:
        print(f"\n💡 RECOMMENDATIONS:")
        for i, rec in enumerate(analysis['recommendations'], 1):
            print(f"   {i}. {rec}")
    
    # Verbose output
    if verbose:
        print(f"\n🔍 DETAILED ANALYSIS:")
        print(json.dumps(analysis, indent=2, default=str))

def main():
    parser = argparse.ArgumentParser(
        description="Extract requirements from job descriptions using AI",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Analyze text from command line
  python cli.py -t "We are looking for a Python developer with 3+ years experience"
  
  # Analyze text from file
  python cli.py -f job_description.txt
  
  # Save results to file
  python cli.py -f job_description.txt -o results.json
  
  # Verbose output
  python cli.py -f job_description.txt -v
        """
    )
    
    # Input options (mutually exclusive)
    input_group = parser.add_mutually_exclusive_group(required=True)
    input_group.add_argument(
        '-t', '--text',
        help='Job description text to analyze'
    )
    input_group.add_argument(
        '-f', '--file',
        help='File containing job description'
    )
    
    # Output options
    parser.add_argument(
        '-o', '--output',
        help='Output file to save results (JSON format)'
    )
    
    # Other options
    parser.add_argument(
        '-v', '--verbose',
        action='store_true',
        help='Verbose output including raw analysis data'
    )
    
    parser.add_argument(
        '--model',
        default='dbmdz/bert-large-cased-finetuned-conll03-english',
        help='Hugging Face model to use (default: dbmdz/bert-large-cased-finetuned-conll03-english)'
    )
    
    parser.add_argument(
        '--confidence',
        type=float,
        default=0.7,
        help='Minimum confidence threshold for entities (default: 0.7)'
    )
    
    args = parser.parse_args()
    
    # Get job description text
    if args.text:
        job_description = args.text
    elif args.file:
        if not Path(args.file).exists():
            print(f"Error: File '{args.file}' not found")
            sys.exit(1)
        job_description = read_file(args.file)
    else:
        print("Error: Must provide either text (-t) or file (-f)")
        sys.exit(1)
    
    if not job_description.strip():
        print("Error: Empty job description")
        sys.exit(1)
    
    try:
        print("🚀 Initializing Job Requirements Extractor...")
        print(f"📚 Using model: {args.model}")
        print(f"🎯 Confidence threshold: {args.confidence}")
        
        # Initialize extractor
        extractor = JobRequirementsExtractor(args.model)
        
        print("🔍 Analyzing job description...")
        
        # Extract requirements
        analysis = extractor.analyze_job_description(job_description)
        
        # Print results
        print_results(analysis, args.verbose)
        
        # Save results if output file specified
        if args.output:
            save_results(analysis, args.output)
        
        print("\n✅ Analysis complete!")
        
    except KeyboardInterrupt:
        print("\n\n⚠️  Analysis interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Error during analysis: {e}")
        if args.verbose:
            import traceback
            traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()
