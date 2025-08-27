#!/usr/bin/env python3
"""
Batch processor for analyzing multiple job descriptions
"""

import os
import json
import csv
from pathlib import Path
from typing import List, Dict, Any
from job_requirements_extractor import JobRequirementsExtractor
import argparse

class BatchJobProcessor:
    def __init__(self, model_name: str = None):
        """Initialize the batch processor."""
        self.extractor = JobRequirementsExtractor(model_name)
        self.results = []
    
    def process_file(self, file_path: str) -> Dict[str, Any]:
        """Process a single job description file."""
        try:
            # Read file content
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Extract requirements
            analysis = self.extractor.analyze_job_description(content)
            
            # Add file metadata
            analysis['file_info'] = {
                'filename': Path(file_path).name,
                'file_path': str(file_path),
                'file_size': len(content)
            }
            
            return analysis
            
        except Exception as e:
            return {
                'error': str(e),
                'file_info': {
                    'filename': Path(file_path).name,
                    'file_path': str(file_path)
                }
            }
    
    def process_directory(self, directory_path: str, file_extensions: List[str] = None) -> List[Dict[str, Any]]:
        """Process all job description files in a directory."""
        if file_extensions is None:
            file_extensions = ['.txt', '.md']
        
        directory = Path(directory_path)
        if not directory.exists() or not directory.is_dir():
            raise ValueError(f"Directory {directory_path} does not exist")
        
        # Find all matching files
        files = []
        for ext in file_extensions:
            files.extend(directory.glob(f"*{ext}"))
        
        print(f"Found {len(files)} files to process")
        
        # Process each file
        results = []
        for i, file_path in enumerate(files, 1):
            print(f"Processing {i}/{len(files)}: {file_path.name}")
            result = self.process_file(str(file_path))
            results.append(result)
        
        self.results = results
        return results
    
    def process_csv(self, csv_path: str, text_column: str = 'description', id_column: str = None) -> List[Dict[str, Any]]:
        """Process job descriptions from a CSV file."""
        if not Path(csv_path).exists():
            raise ValueError(f"CSV file {csv_path} does not exist")
        
        results = []
        
        with open(csv_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            
            for i, row in enumerate(reader, 1):
                if text_column not in row:
                    raise ValueError(f"Column '{text_column}' not found in CSV")
                
                print(f"Processing row {i}: {row.get(id_column, f'Row {i}')}")
                
                # Extract requirements
                analysis = self.extractor.analyze_job_description(row[text_column])
                
                # Add row metadata
                analysis['row_info'] = {
                    'row_number': i,
                    'row_id': row.get(id_column, f'Row_{i}'),
                    'all_columns': row
                }
                
                results.append(analysis)
        
        self.results = results
        return results
    
    def save_results(self, output_path: str, format: str = 'json'):
        """Save results to a file."""
        if format.lower() == 'json':
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(self.results, f, indent=2, default=str)
        
        elif format.lower() == 'csv':
            # Flatten results for CSV export
            flattened_results = []
            for result in self.results:
                flat_row = {}
                
                # Add file/row info
                if 'file_info' in result:
                    flat_row.update({
                        'filename': result['file_info']['filename'],
                        'file_path': result['file_info']['file_path']
                    })
                elif 'row_info' in result:
                    flat_row.update({
                        'row_id': result['row_info']['row_id'],
                        'row_number': result['row_info']['row_number']
                    })
                
                # Add basic metrics
                flat_row.update({
                    'text_length': result.get('text_length', 0),
                    'word_count': result.get('word_count', 0),
                    'complexity_score': result.get('complexity_score', 0)
                })
                
                # Add requirements summary
                if 'requirements' in result and 'summary' in result['requirements']:
                    summary = result['requirements']['summary']
                    flat_row.update({
                        'total_sentences': summary.get('total_sentences', 0),
                        'requirement_sentences': summary.get('requirement_sentences', 0),
                        'requirement_density': summary.get('requirement_density', 0),
                        'estimated_requirements': summary.get('estimated_requirements', 0)
                    })
                
                # Add categorized requirements count
                if 'requirements' in result and 'categorized_requirements' in result['requirements']:
                    cats = result['requirements']['categorized_requirements']
                    for category, items in cats.items():
                        flat_row[f'{category}_count'] = len(items)
                
                flattened_results.append(flat_row)
            
            # Write CSV
            if flattened_results:
                fieldnames = flattened_results[0].keys()
                with open(output_path, 'w', newline='', encoding='utf-8') as f:
                    writer = csv.DictWriter(f, fieldnames=fieldnames)
                    writer.writeheader()
                    writer.writerows(flattened_results)
        
        print(f"Results saved to {output_path}")
    
    def generate_summary_report(self) -> Dict[str, Any]:
        """Generate a summary report of all processed jobs."""
        if not self.results:
            return {"error": "No results to summarize"}
        
        # Calculate aggregate statistics
        total_files = len(self.results)
        successful_analyses = len([r for r in self.results if 'error' not in r])
        failed_analyses = total_files - successful_analyses
        
        # Aggregate metrics
        total_text_length = sum(r.get('text_length', 0) for r in self.results if 'error' not in r)
        total_word_count = sum(r.get('word_count', 0) for r in self.results if 'error' not in r)
        avg_complexity = sum(r.get('complexity_score', 0) for r in self.results if 'error' not in r) / successful_analyses if successful_analyses > 0 else 0
        
        # Requirements summary
        total_requirements = 0
        category_counts = {}
        
        for result in self.results:
            if 'error' not in result and 'requirements' in result:
                reqs = result['requirements']
                
                if 'summary' in reqs:
                    total_requirements += reqs['summary'].get('estimated_requirements', 0)
                
                if 'categorized_requirements' in reqs:
                    cats = reqs['categorized_requirements']
                    for category, items in cats.items():
                        if category not in category_counts:
                            category_counts[category] = 0
                        category_counts[category] += len(items)
        
        summary = {
            'total_files_processed': total_files,
            'successful_analyses': successful_analyses,
            'failed_analyses': failed_analyses,
            'success_rate': successful_analyses / total_files if total_files > 0 else 0,
            'aggregate_metrics': {
                'total_text_length': total_text_length,
                'total_word_count': total_word_count,
                'average_complexity_score': round(avg_complexity, 2)
            },
            'requirements_summary': {
                'total_requirements_found': total_requirements,
                'average_requirements_per_job': round(total_requirements / successful_analyses, 2) if successful_analyses > 0 else 0
            },
            'category_distribution': category_counts
        }
        
        return summary

def main():
    parser = argparse.ArgumentParser(
        description="Batch process multiple job descriptions",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Process all .txt files in a directory
  python batch_processor.py -d jobs/ -o results.json
  
  # Process CSV file
  python batch_processor.py -c jobs.csv -o results.csv --format csv
  
  # Process specific file types
  python batch_processor.py -d jobs/ -e .txt .md -o results.json
        """
    )
    
    # Input options
    input_group = parser.add_mutually_exclusive_group(required=True)
    input_group.add_argument(
        '-d', '--directory',
        help='Directory containing job description files'
    )
    input_group.add_argument(
        '-c', '--csv',
        help='CSV file containing job descriptions'
    )
    
    # Output options
    parser.add_argument(
        '-o', '--output',
        required=True,
        help='Output file path'
    )
    
    parser.add_argument(
        '--format',
        choices=['json', 'csv'],
        default='json',
        help='Output format (default: json)'
    )
    
    # Processing options
    parser.add_argument(
        '-e', '--extensions',
        nargs='+',
        default=['.txt', '.md'],
        help='File extensions to process (default: .txt .md)'
    )
    
    parser.add_argument(
        '--text-column',
        default='description',
        help='CSV column containing job descriptions (default: description)'
    )
    
    parser.add_argument(
        '--id-column',
        help='CSV column to use as row identifier'
    )
    
    parser.add_argument(
        '--model',
        help='Hugging Face model to use'
    )
    
    parser.add_argument(
        '--summary',
        action='store_true',
        help='Generate and display summary report'
    )
    
    args = parser.parse_args()
    
    try:
        print("🚀 Initializing Batch Job Processor...")
        
        # Initialize processor
        processor = BatchJobProcessor(args.model)
        
        # Process files
        if args.directory:
            print(f"📁 Processing directory: {args.directory}")
            results = processor.process_directory(args.directory, args.extensions)
        
        elif args.csv:
            print(f"📊 Processing CSV file: {args.csv}")
            results = processor.process_csv(args.csv, args.text_column, args.id_column)
        
        print(f"✅ Processed {len(results)} items")
        
        # Save results
        output_ext = Path(args.output).suffix.lower()
        if output_ext == '.csv':
            format_type = 'csv'
        elif output_ext == '.json':
            format_type = 'json'
        else:
            format_type = args.format
        
        processor.save_results(args.output, format_type)
        
        # Generate summary if requested
        if args.summary:
            print("\n📊 SUMMARY REPORT")
            print("=" * 50)
            
            summary = processor.generate_summary_report()
            
            if 'error' not in summary:
                print(f"📁 Total files processed: {summary['total_files_processed']}")
                print(f"✅ Successful analyses: {summary['successful_analyses']}")
                print(f"❌ Failed analyses: {summary['failed_analyses']}")
                print(f"📈 Success rate: {summary['success_rate']:.1%}")
                
                metrics = summary['aggregate_metrics']
                print(f"\n📊 Aggregate Metrics:")
                print(f"   Total text length: {metrics['total_text_length']:,} characters")
                print(f"   Total word count: {metrics['total_word_count']:,} words")
                print(f"   Average complexity: {metrics['average_complexity_score']}/10")
                
                req_summary = summary['requirements_summary']
                print(f"\n🔍 Requirements Summary:")
                print(f"   Total requirements found: {req_summary['total_requirements_found']}")
                print(f"   Average per job: {req_summary['average_requirements_per_job']}")
                
                if summary['category_distribution']:
                    print(f"\n🏷️  Category Distribution:")
                    for category, count in summary['category_distribution'].items():
                        print(f"   {category.replace('_', ' ').title()}: {count}")
            else:
                print(f"❌ Error generating summary: {summary['error']}")
        
        print(f"\n🎉 Batch processing complete! Results saved to {args.output}")
        
    except Exception as e:
        print(f"❌ Error during batch processing: {e}")
        import traceback
        traceback.print_exc()
        exit(1)

if __name__ == "__main__":
    main()
