"""
AI Resume Tailor - Main Streamlit Application
A web app that helps job seekers tailor their resumes using AI
"""
import streamlit as st
from utils import extract_text_from_pdf, get_ai_suggestions, parse_ai_response


# Page configuration
st.set_page_config(
    page_title="AI Resume Tailor",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

    :root {
        --bg: #ffffff;
        --surface: #f8f9fa;
        --border: #e9ecef;
        --text: #212529;
        --text-muted: #6c757d;
        --accent: #2563eb;
        --success: #059669;
        --warning: #d97706;
        --danger: #dc2626;
    }

    * { font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif; }

    .stApp { background: var(--bg); }

    .block-container { max-width: 800px; padding-top: 2rem; padding-bottom: 2rem; }

    /* Header */
    .app-header {
        text-align: center;
        padding: 3rem 0 2rem;
    }
    .app-header h1 {
        font-size: 2.5rem;
        font-weight: 700;
        color: var(--text);
        letter-spacing: -0.03em;
        margin-bottom: 0.5rem;
    }
    .app-header p {
        font-size: 1.1rem;
        color: var(--text-muted);
        font-weight: 400;
    }

    /* Section headers */
    .section-header {
        font-size: 1rem;
        font-weight: 600;
        color: var(--text);
        margin-bottom: 0.5rem;
        letter-spacing: -0.01em;
    }
    .section-subtitle {
        font-size: 0.875rem;
        color: var(--text-muted);
        margin-bottom: 1rem;
    }

    /* Input styling */
    .stTextArea textarea {
        border: 1px solid var(--border) !important;
        border-radius: 8px !important;
        font-size: 0.9rem !important;
        padding: 0.875rem !important;
        background: var(--surface) !important;
        color: var(--text) !important;
    }
    .stTextArea textarea::placeholder {
        color: var(--text-muted) !important;
    }
    .stTextArea textarea:disabled {
        color: var(--text) !important;
        opacity: 0.8 !important;
    }
    .stTextArea textarea:focus {
        border-color: var(--accent) !important;
        box-shadow: 0 0 0 2px rgba(37,99,235,0.1) !important;
    }

    /* Primary button */
    .stButton > button {
        background: var(--text) !important;
        color: white !important;
        font-weight: 500 !important;
        padding: 0.625rem 1.5rem !important;
        border-radius: 6px !important;
        border: none !important;
        font-size: 0.9rem !important;
    }
    .stButton > button:hover {
        background: #343a40 !important;
    }
    .primary-btn > button {
        background: var(--accent) !important;
        font-size: 1rem !important;
        padding: 0.75rem 2rem !important;
    }
    .primary-btn > button:hover {
        background: #1d4ed8 !important;
    }

    /* File uploader */
    .stFileUploader {
        border: 2px dashed var(--border) !important;
        border-radius: 8px !important;
        padding: 1.5rem !important;
        background: var(--surface) !important;
    }
    .stFileUploader > div > div:first-child p {
        color: var(--text) !important;
    }
    .stFileUploader span {
        color: white !important;
    }

    /* Expander - consolidated and fixed */
    div[data-testid="stExpander"] {
        background: var(--surface) !important;
        border: 1px solid var(--border);
        border-radius: 8px;
        overflow: hidden;
    }
    div[data-testid="stExpanderHeader"] {
        background: #1a1a2e !important;
        color: white !important;
    }
    div[data-testid="stExpanderHeader"]:hover {
        background: #1a1a2e !important;
        color: white !important;
    }
    div[data-testid="stExpanderContent"] {
        background: var(--bg) !important;
        padding: 1rem;
    }
    
    /* Force textarea inside expander to be readable */
    div[data-testid="stExpander"] div[data-testid="stTextArea"] textarea,
    div[data-testid="stExpander"] div[data-testid="stTextArea"] textarea:disabled,
    div[data-testid="stExpanderContent"] .stTextArea textarea,
    div[data-testid="stExpanderContent"] .stTextArea textarea:disabled {
        background-color: #ffffff !important;
        color: #000000 !important;
        -webkit-text-fill-color: #000000 !important;
        opacity: 1 !important;
        caret-color: #000000 !important;
    }

    /* Progress bar */
    .stProgress > div > div > div {
        background-color: var(--accent) !important;
    }

    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        border-bottom: 1px solid var(--border);
    }
    .stTabs [data-baseweb="tab-list"] button {
        font-weight: 500;
        font-size: 0.875rem;
        color: var(--text-muted) !important;
    }
    .stTabs [data-baseweb="tab-list"] button[aria-selected="true"] {
        color: var(--accent) !important;
        border-bottom: 2px solid var(--accent);
    }

    /* Selectbox dropdown */
    .stSelectbox label {
        color: var(--text) !important;
    }

    /* Radio/Checkbox */
    .stRadio label, .stCheckbox label {
        color: var(--text) !important;
    }

    /* Number input */
    .stNumberInput input {
        color: var(--text) !important;
    }

    /* Input fields general */
    .stTextInput input {
        color: var(--text) !important;
        background: var(--surface) !important;
    }
    .stTextInput input::placeholder {
        color: var(--text-muted) !important;
    }

    /* All form labels */
    .stForm label, .stForm fieldset legend {
        color: var(--text) !important;
    }

    /* Cards */
    .card {
        background: var(--surface);
        border: 1px solid var(--border);
        border-radius: 8px;
        padding: 1.25rem;
    }

    /* Score section */
    .score-box {
        background: linear-gradient(135deg, #1a1a1a 0%, #2d2d2d 100%);
        color: white;
        border-radius: 12px;
        padding: 2rem;
        text-align: center;
    }
    .score-number { font-size: 3rem; font-weight: 700; }
    .score-label { font-size: 0.75rem; opacity: 0.7; margin-top: 0.5rem; text-transform: uppercase; letter-spacing: 0.1em; }

    /* Improvement boxes */
    .original-box {
        background: #fef2f2;
        border-left: 3px solid var(--danger);
        padding: 0.875rem 1rem;
        border-radius: 0 6px 6px 0;
        font-size: 0.875rem;
        color: #991b1b;
    }
    .improved-box {
        background: #f0fdf4;
        border-left: 3px solid var(--success);
        padding: 0.875rem 1rem;
        border-radius: 0 6px 6px 0;
        font-size: 0.875rem;
        color: #166534;
        font-weight: 500;
    }
    .tip-box {
        background: #eff6ff;
        border-left: 3px solid var(--accent);
        padding: 0.875rem 1rem;
        border-radius: 0 6px 6px 0;
        font-size: 0.875rem;
    }

    /* Keyword badges */
    .badge {
        display: inline-block;
        padding: 0.25rem 0.75rem;
        border-radius: 4px;
        font-size: 0.8rem;
        font-weight: 500;
        margin: 0.2rem;
    }
    .badge-must { background: #fef2f2; color: var(--danger); }
    .badge-nice { background: #fffbeb; color: var(--warning); }
    .badge-add { background: #f0fdf4; color: var(--success); }
    .badge-remove { background: var(--surface); color: var(--text-muted); }

    /* Divider */
    hr { border: none; height: 1px; background: var(--border); margin: 2.5rem 0; }

    /* Footer */
    .app-footer {
        text-align: center;
        padding: 2.5rem 0 1rem;
        color: var(--text-muted);
        font-size: 0.8rem;
        border-top: 1px solid var(--border);
        margin-top: 2rem;
    }

    /* Status indicators */
    .status-strong { color: var(--success); }
    .status-moderate { color: var(--warning); }
    .status-weak { color: var(--danger); }

    /* Progress bar */
    .stProgress > div > div { background-color: var(--accent) !important; }

    /* Success/info styling */
    .stSuccess, .stInfo, .stWarning, .stError { border-radius: 6px !important; }

    /* Spinner */
    .stSpinner { color: var(--accent) !important; }

    [data-testid="stSidebar"] { display: none; }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'results' not in st.session_state:
    st.session_state.results = None
if 'input_method' not in st.session_state:
    st.session_state.input_method = "Upload PDF"


def main():
    st.markdown("""
    <div class="app-header">
        <h1>AI Resume Tailor</h1>
        <p>Tailor your resume for any job description with AI-powered analysis</p>
    </div>
    """, unsafe_allow_html=True)

    with st.container():
        st.markdown('<div class="section-header">Your Resume</div>', unsafe_allow_html=True)
        st.markdown('<div class="section-subtitle">Upload a PDF or paste your resume text</div>', unsafe_allow_html=True)

        resume_text = ""

        if st.session_state.input_method == "Upload PDF":
            uploaded_file = st.file_uploader("Choose a PDF file", type=["pdf"], label_visibility="collapsed")
            if uploaded_file is not None:
                try:
                    with st.spinner("Extracting text from PDF..."):
                        resume_text = extract_text_from_pdf(uploaded_file)
                        st.success("PDF extracted successfully")
                        with st.expander("Preview extracted text"):
                            st.text_area(
                                "Resume preview",
                                value=resume_text[:1000] + ("..." if len(resume_text) > 1000 else ""),
                                height=150,
                                disabled=True,
                                label_visibility="collapsed"
                            )
                except Exception as e:
                    st.error(f"Error reading PDF: {str(e)}")
        else:
            resume_text = st.text_area(
                "Resume text",
                height=200,
                placeholder="Paste your complete resume content here...",
                label_visibility="collapsed"
            )

    with st.container():
        st.markdown('<div class="section-header">Job Description</div>', unsafe_allow_html=True)
        st.markdown('<div class="section-subtitle">Paste the job description you are applying for</div>', unsafe_allow_html=True)

        job_description = st.text_area(
            "Job description",
            height=200,
            placeholder="Paste the job description here...",
            label_visibility="collapsed"
        )

    st.markdown("<hr>", unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("Analyze Resume", use_container_width=True, type="primary"):
            if not resume_text or not resume_text.strip():
                st.error("Please provide your resume")
            elif not job_description or not job_description.strip():
                st.error("Please paste the job description")
            else:
                with st.spinner("Analyzing your resume..."):
                    try:
                        ai_response = get_ai_suggestions(resume_text, job_description)
                        st.session_state.results = parse_ai_response(ai_response)
                        st.success("Analysis complete")
                        st.balloons()
                    except ValueError as e:
                        st.error(f"Configuration Error: {str(e)}")
                    except Exception as e:
                        st.error(f"Error during analysis: {str(e)}")

    # Results
    if st.session_state.results:
        st.markdown("<hr>", unsafe_allow_html=True)
        st.markdown('<div class="section-header">📊 Analysis Results</div>', unsafe_allow_html=True)

        results = st.session_state.results

        # ATS Score
        try:
            percentage = int(results['ats_score']['percentage'])
        except:
            percentage = 0

        col1, col2 = st.columns([1, 2])

        with col1:
            st.markdown(f"""
            <div class="score-box">
                <div class="score-number">{percentage}%</div>
                <div class="score-label">ATS Match Score</div>
            </div>
            """, unsafe_allow_html=True)

        with col2:
            if percentage >= 80:
                status_class = "status-strong"
                status_text = "Strong Match"
                status_msg = "Your resume aligns well with this role. You're ready to apply."
            elif percentage >= 60:
                status_class = "status-moderate"
                status_text = "Moderate Match"
                status_msg = "Good foundation. Apply the suggestions below to improve further."
            else:
                status_class = "status-weak"
                status_text = "Needs Improvement"
                status_msg = "Significant gaps detected. Follow the recommendations below."

            st.markdown(f"### {status_text}")
            st.progress(percentage / 100)
            st.markdown(f"_{status_msg}_")
            if results['ats_score'].get('reason'):
                st.markdown(f"<div style='color: var(--text-muted); font-size: 0.9rem; margin-top: 0.5rem;'><b>Key factor:</b> {results['ats_score']['reason']}</div>", unsafe_allow_html=True)

        st.markdown("<hr>", unsafe_allow_html=True)

        # Tabs
        tab1, tab2, tab3, tab4 = st.tabs(["Bullet Points", "Keywords", "Summary", "Skills"])

        # Tab 1: Bullets
        with tab1:
            st.markdown('<div class="section-header">Bullet Point Improvements</div>', unsafe_allow_html=True)
            st.markdown('<div class="section-subtitle">Make your achievements more impactful and ATS-friendly</div>', unsafe_allow_html=True)

            if results.get('bullet_improvements'):
                for i, bullet in enumerate(results['bullet_improvements'], 1):
                    st.markdown(f"**Bullet Point {i}**")

                    st.markdown(f"""
                    <div class="original-box">
                        <b>Original:</b><br>{bullet['original']}
                    </div>
                    """, unsafe_allow_html=True)

                    st.markdown(f"""
                    <div class="improved-box">
                        <b>Improved:</b><br>{bullet['improved']}
                    </div>
                    """, unsafe_allow_html=True)

                    if bullet.get('reason'):
                        st.markdown(f'<div class="tip-box"><b>Why this works:</b> {bullet["reason"]}</div>', unsafe_allow_html=True)

                    st.markdown("<br>", unsafe_allow_html=True)
            else:
                st.success("Your bullet points are already well-optimized.")

        # Tab 2: Keywords
        with tab2:
            st.markdown('<div class="section-header">Missing Keywords</div>', unsafe_allow_html=True)
            st.markdown('<div class="section-subtitle">Add these job-specific terms to improve your ATS ranking</div>', unsafe_allow_html=True)

            keywords = results.get('missing_keywords', {})

            if keywords.get('must_add'):
                st.markdown("**High Priority**")
                badges = "".join([f'<span class="badge badge-must">{k}</span>' for k in keywords['must_add']])
                st.markdown(f'<div>{badges}</div>', unsafe_allow_html=True)

            if keywords.get('nice_to_add'):
                st.markdown("**Recommended**")
                badges = "".join([f'<span class="badge badge-nice">{k}</span>' for k in keywords['nice_to_add']])
                st.markdown(f'<div>{badges}</div>', unsafe_allow_html=True)

            st.markdown("""
            <div class="tip-box">
                Add keywords naturally within bullet points, include them in your skills section, and weave them into your professional summary where relevant.
            </div>
            """, unsafe_allow_html=True)

        # Tab 3: Summary
        with tab3:
            st.markdown('<div class="section-header">Professional Summary</div>', unsafe_allow_html=True)
            st.markdown('<div class="section-subtitle">Tailored summary for this specific role</div>', unsafe_allow_html=True)

            summary = results.get('summary_suggestion', {})

            col1, col2 = st.columns(2)

            if summary.get('current'):
                with col1:
                    st.markdown("**Current**")
                    st.markdown(f"""
                    <div style="background: var(--surface); padding: 1rem; border-radius: 6px; border: 1px solid var(--border); font-size: 0.875rem; line-height: 1.6;">
                        {summary['current']}
                    </div>
                    """, unsafe_allow_html=True)

            if summary.get('suggested'):
                with col2:
                    st.markdown("**Suggested**")
                    st.markdown(f"""
                    <div style="background: #f0fdf4; padding: 1rem; border-radius: 6px; border: 1px solid #bbf7d0; font-size: 0.875rem; line-height: 1.6; color: #166534;">
                        {summary['suggested']}
                    </div>
                    """, unsafe_allow_html=True)

        # Tab 4: Skills
        with tab4:
            st.markdown('<div class="section-header">Skills Optimization</div>', unsafe_allow_html=True)
            st.markdown('<div class="section-subtitle">Adjust your skills section for better alignment</div>', unsafe_allow_html=True)

            skills = results.get('skills_suggestion', {})

            col1, col2 = st.columns(2)

            with col1:
                if skills.get('add'):
                    st.markdown("**Add These Skills**")
                    badges = "".join([f'<span class="badge badge-add">+ {s}</span>' for s in skills['add']])
                    st.markdown(f'<div>{badges}</div>', unsafe_allow_html=True)
                else:
                    st.success("All relevant skills are present.")

            with col2:
                if skills.get('remove'):
                    st.markdown("**Consider Removing**")
                    badges = "".join([f'<span class="badge badge-remove">- {s}</span>' for s in skills['remove']])
                    st.markdown(f'<div>{badges}</div>', unsafe_allow_html=True)
                else:
                    st.info("All listed skills appear relevant.")

        st.markdown("<hr>", unsafe_allow_html=True)

        st.markdown('<div class="section-header">Next Steps</div>', unsafe_allow_html=True)

        c1, c2, c3 = st.columns(3)
        with c1:
            st.markdown("""
            <div class="card" style="text-align: center;">
                <div style="font-size: 1.25rem; margin-bottom: 0.5rem;">1</div>
                <div style="font-weight: 600;">Update Resume</div>
                <div style="font-size: 0.8rem; color: var(--text-muted); margin-top: 0.25rem;">Apply the AI suggestions</div>
            </div>
            """, unsafe_allow_html=True)
        with c2:
            st.markdown("""
            <div class="card" style="text-align: center;">
                <div style="font-size: 1.25rem; margin-bottom: 0.5rem;">2</div>
                <div style="font-weight: 600;">Review & Refine</div>
                <div style="font-size: 0.8rem; color: var(--text-muted); margin-top: 0.25rem;">Personalize with your voice</div>
            </div>
            """, unsafe_allow_html=True)
        with c3:
            st.markdown("""
            <div class="card" style="text-align: center;">
                <div style="font-size: 1.25rem; margin-bottom: 0.5rem;">3</div>
                <div style="font-weight: 600;">Apply with Confidence</div>
                <div style="font-size: 0.8rem; color: var(--text-muted); margin-top: 0.25rem;">Submit your tailored resume</div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        if st.button("Analyze Another Job", use_container_width=True):
            st.session_state.results = None
            st.rerun()

    # Footer
    st.markdown("""
    <div class="app-footer">
        AI Resume Tailor · Built to help job seekers land more interviews
    </div>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()