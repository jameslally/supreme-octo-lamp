import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from job_requirements_extractor import JobRequirementsExtractor
import json

# Page configuration
st.set_page_config(
    page_title="Job Requirements Extractor",
    page_icon="💼",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #1f77b4;
    }
    .requirement-item {
        background-color: #ffffff;
        padding: 0.5rem;
        margin: 0.5rem 0;
        border-radius: 0.3rem;
        border: 1px solid #e0e0e0;
    }
</style>
""", unsafe_allow_html=True)

def main():
    # Header
    st.markdown('<h1 class="main-header">💼 Job Requirements Extractor</h1>', unsafe_allow_html=True)
    st.markdown("### Extract and analyze requirements from job descriptions using AI")
    
    # Sidebar
    st.sidebar.title("Settings")
    model_option = st.sidebar.selectbox(
        "Choose Model",
        ["dbmdz/bert-large-cased-finetuned-conll03-english", "microsoft/DialoGPT-medium"],
        help="Select the Hugging Face model to use for extraction"
    )
    
    confidence_threshold = st.sidebar.slider(
        "Entity Confidence Threshold",
        min_value=0.0,
        max_value=1.0,
        value=0.7,
        step=0.1,
        help="Minimum confidence score for extracted entities"
    )
    
    # Main content area
    tab1, tab2, tab3 = st.tabs(["📝 Extract Requirements", "📊 Analysis Dashboard", "ℹ️ About"])
    
    with tab1:
        st.header("Extract Job Requirements")
        
        # Input method selection
        input_method = st.radio(
            "Choose input method:",
            ["📝 Paste Job Description", "📁 Upload File", "💡 Use Sample"]
        )
        
        job_description = ""
        
        if input_method == "📝 Paste Job Description":
            job_description = st.text_area(
                "Paste your job description here:",
                height=300,
                placeholder="Enter the job description text here..."
            )
        
        elif input_method == "📁 Upload File":
            uploaded_file = st.file_uploader(
                "Upload a text file with job description:",
                type=['txt', 'md', 'docx'],
                help="Supported formats: .txt, .md, .docx"
            )
            
            if uploaded_file is not None:
                try:
                    if uploaded_file.name.endswith('.txt') or uploaded_file.name.endswith('.md'):
                        job_description = str(uploaded_file.read(), "utf-8")
                    else:
                        st.error("Please upload a .txt or .md file for now.")
                except Exception as e:
                    st.error(f"Error reading file: {e}")
        
        elif input_method == "💡 Use Sample":
            sample_job = """
            Senior Software Engineer
            
            We are looking for a Senior Software Engineer to join our dynamic team. 
            The ideal candidate must have at least 5+ years of experience in software development.
            
            Required Skills:
            • Proficient in Python, Java, and JavaScript
            • Experience with AWS cloud services
            • Knowledge of Docker and Kubernetes
            • Strong understanding of database design and SQL
            • Experience with agile methodologies
            • Git version control and CI/CD pipelines
            • RESTful API design and development
            
            Preferred Qualifications:
            • Master's degree in Computer Science or related field
            • Experience with machine learning frameworks (TensorFlow, PyTorch)
            • Knowledge of microservices architecture
            • Leadership experience in technical teams
            • Experience with monitoring tools (Prometheus, Grafana)
            • Knowledge of security best practices
            
            The candidate should have excellent communication skills and be able to work in a fast-paced environment.
            """
            job_description = st.text_area("Sample Job Description:", value=sample_job, height=300)
        
        # Extract button
        if st.button("🚀 Extract Requirements", type="primary", use_container_width=True):
            if job_description.strip():
                with st.spinner("Analyzing job description..."):
                    try:
                        # Initialize extractor
                        extractor = JobRequirementsExtractor(model_option)
                        
                        # Extract requirements
                        analysis = extractor.analyze_job_description(job_description)
                        
                        # Display results
                        display_results(analysis)
                        
                    except Exception as e:
                        st.error(f"Error during extraction: {e}")
                        st.info("Please check your input and try again.")
            else:
                st.warning("Please enter a job description first.")
    
    with tab2:
        st.header("Analysis Dashboard")
        st.info("Extract requirements first to see the analysis dashboard.")
    
    with tab3:
        st.header("About This Application")
        st.markdown("""
        ### What is Job Requirements Extractor?
        
        This application uses advanced Natural Language Processing (NLP) models from Hugging Face to automatically extract and categorize requirements from job descriptions.
        
        ### Features:
        - **Text Pattern Recognition**: Identifies common requirement patterns using regex
        - **Named Entity Recognition (NER)**: Extracts entities like skills, experience levels, and qualifications
        - **Categorization**: Organizes requirements into logical categories
        - **Complexity Analysis**: Provides insights into job difficulty
        - **Recommendations**: Offers personalized advice based on extracted requirements
        
        ### How it works:
        1. **Input**: Paste or upload a job description
        2. **Processing**: The AI model analyzes the text using multiple techniques
        3. **Extraction**: Requirements are identified and categorized
        4. **Analysis**: Comprehensive insights and recommendations are generated
        
        ### Models Used:
        - **BERT-based NER**: For entity extraction
        - **Sentence Transformers**: For semantic understanding
        - **Pattern Matching**: For requirement identification
        
        ### Use Cases:
        - Job seekers analyzing requirements
        - HR professionals reviewing job postings
        - Career counselors providing guidance
        - Resume optimization
        """)

def display_results(analysis):
    """Display the analysis results in an organized way."""
    st.success("✅ Analysis complete!")
    
    # Create columns for metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Text Length", f"{analysis.get('text_length', 0):,} chars")
    
    with col2:
        st.metric("Word Count", f"{analysis.get('word_count', 0):,} words")
    
    with col3:
        st.metric("Complexity Score", f"{analysis.get('complexity_score', 0):.1f}/10")
    
    with col4:
        requirements = analysis.get('requirements', {})
        summary = requirements.get('summary', {})
        st.metric("Requirements Found", summary.get('estimated_requirements', 0))
    
    # Requirements section
    st.subheader("📋 Extracted Requirements")
    
    requirements = analysis.get('requirements', {})
    
    # Individual requirements (bullet points and lists)
    if 'individual_requirements' in requirements and requirements['individual_requirements']:
        st.write(f"**🔹 Extracted Requirements: {len(requirements['individual_requirements'])} found**")
        for i, req in enumerate(requirements['individual_requirements'], 1):
            st.markdown(f"{i}. {req}")
    
    # Categorized requirements
    if 'categorized_requirements' in requirements and requirements['categorized_requirements']:
        st.subheader("🏷️ Categorized Requirements")
        
        cats = requirements['categorized_requirements']
        
        # Create columns for categories
        cols = st.columns(min(len(cats), 3))
        
        for i, (category, items) in enumerate(cats.items()):
            col_idx = i % 3
            with cols[col_idx]:
                st.markdown(f"**{category.replace('_', ' ').title()} ({len(items)} items)**")
                for item in items:  # Show all items
                    st.markdown(f"• {item}")
    
    # Summary statistics
    if 'summary' in requirements:
        st.subheader("📊 Summary Statistics")
        
        summary = requirements['summary']
        
        # Create a bar chart for summary
        summary_data = {
            'Metric': ['Total Sentences', 'Requirement Sentences', 'Requirement Density'],
            'Value': [
                summary.get('total_sentences', 0),
                summary.get('requirement_sentences', 0),
                round(summary.get('requirement_density', 0) * 100, 1)
            ]
        }
        
        df_summary = pd.DataFrame(summary_data)
        fig = px.bar(df_summary, x='Metric', y='Value', 
                    title="Job Description Analysis Summary",
                    color='Value', color_continuous_scale='Blues')
        st.plotly_chart(fig, use_container_width=True)
    
    # Recommendations
    if 'recommendations' in analysis and analysis['recommendations']:
        st.subheader("💡 Recommendations")
        
        for i, rec in enumerate(analysis['recommendations'], 1):
            st.info(f"{i}. {rec}")
    
    # Download results
    st.subheader("💾 Download Results")
    
    # Create JSON for download
    json_str = json.dumps(analysis, indent=2, default=str)
    
    st.download_button(
        label="📥 Download Analysis (JSON)",
        data=json_str,
        file_name="job_requirements_analysis.json",
        mime="application/json"
    )
    
    # Show raw data in expander
    with st.expander("🔍 View Raw Analysis Data"):
        st.json(analysis)

if __name__ == "__main__":
    main()
