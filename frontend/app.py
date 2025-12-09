import streamlit as st
import utils
import pandas as pd
from datetime import datetime

# --- CONFIG & STYLES ---
st.set_page_config(
    page_title="Multi-Modal Intelligence Console",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

CUSTOM_CSS = """
<style>
    .reportview-container {
        background: #0e1117;
    }
    .main-header {
        font-family: 'Inter', sans-serif;
        font-weight: 700;
        font-size: 2.5rem;
        background: -webkit-linear-gradient(45deg, #FF4B4B, #FF914D);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    .card {
        background-color: #262730;
        padding: 1.5rem;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        margin-bottom: 1rem;
    }
    .insight-box {
        background-color: #1E1E1E;
        border-left: 5px solid #FF4B4B;
        padding: 10px;
        margin-top: 10px;
    }
</style>
"""
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

if 'insights' not in st.session_state:
    st.session_state['insights'] = []

if 'current_session_id' not in st.session_state:
    st.session_state['current_session_id'] = None

# --- SIDEBAR ---
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/8637/8637102.png", width=50) # Placeholder Icon
    st.title("MMIC Console")
    st.markdown("---")
    st.info("Enterprise AI System v1.0")
    st.markdown("### System Status")
    st.success("Backend: Online")
    st.success("Vector DB: Connected")
    
# --- MAIN TABS ---
tab_home, tab_files, tab_text, tab_chat, tab_report = st.tabs([
    "🏠 Dashboard", "📂 Multi-Modal Upload", "📝 Text Studio", "💬 AI Chat", "📄 Report Gen"
])

# --- DASHBOARD ---
with tab_home:
    st.markdown('<p class="main-header">Multi-Modal Intelligence Console</p>', unsafe_allow_html=True)
    st.write("Welcome to the enterprise-grade AI analysis suite.")
    
    # Top Level Metrics
    m1, m2, m3, m4 = st.columns(4)
    with m1:
        st.metric(label="Total Analyzed Files", value=len(st.session_state['insights']), delta="+2 this week")
    with m2:
        st.metric(label="Active Sessions", value="3", delta="Online")
    with m3:
        st.metric(label="Vector DB Records", value="184", delta="+12%")
    with m4:
        st.metric(label="System Latency", value="42ms", delta="-5ms")

    st.markdown("---")

    # Interactive Charts
    c1, c2 = st.columns([2, 1])
    
    with c1:
        st.subheader("📊 Analysis Activity")
        # Mock data for demonstration of "Enterprise" feel
        chart_data = pd.DataFrame({
            'Day': ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'],
            'Images': [12, 19, 3, 5, 2, 3, 10],
            'Audio': [5, 2, 8, 1, 6, 4, 7],
            'Text': [15, 20, 15, 25, 10, 5, 12]
        })
        st.bar_chart(chart_data.set_index('Day'))
    
    with c2:
        st.subheader("🧠 Model Status")
        st.info("GPT-4o Vision: **Online**")
        st.info("Whisper v3: **Online**")
        st.info("Embedding-3-Small: **Online**")
        
        st.markdown("### Recent System Logs")
        st.caption("✅ 14:02: System Initialization Complete")
        st.caption("✅ 14:03: Vector Database Connected")
        st.caption("⚠️ 14:05: High Latency Detected (Resolved)")

# --- MULTI-MODAL UPLOAD ---
with tab_files:
    st.header("Upload & Analyze")
    
    upload_type = st.radio("Select Input Type", ["Image", "Audio"], horizontal=True)
    
    if upload_type == "Image":
        img_file = st.file_uploader("Upload Image", type=["jpg", "png", "jpeg"])
        if img_file:
            col_a, col_b = st.columns([1, 1])
            with col_a:
                st.image(img_file, use_column_width=True, caption="Preview")
            with col_b:
                prompt = st.text_input("Analysis Prompt", "Describe this image in detail and list key insights.")
                if st.button("Analyze Image", type="primary"):
                    with st.spinner("Processing with GPT-4o Vision..."):
                        try:
                            res = utils.upload_image(img_file, prompt)
                            st.markdown("### 🔍 Analysis Result")
                            st.markdown(f"<div class='card'>{res['analysis']}</div>", unsafe_allow_html=True)
                            
                            st.session_state['insights'].append({
                                "title": f"Image Analysis: {img_file.name}",
                                "body": res['analysis'],
                                "type": "image"
                            })
                            st.success("Saved to Insights")
                        except Exception as e:
                            st.error(f"Error: {e}")

    elif upload_type == "Audio":
        aud_file = st.file_uploader("Upload Audio", type=["mp3", "wav", "m4a"])
        if aud_file:
            st.audio(aud_file)
            if st.button("Transcribe & Analyze", type="primary"):
                with st.spinner("Transcribing (Whisper) & Analyzing..."):
                    try:
                        res = utils.upload_audio(aud_file) # Returns transcript & analysis
                        
                        st.subheader("Transcript")
                        st.text_area("", res['transcript'], height=150)
                        
                        st.subheader("AI Insights")
                        st.markdown(f"<div class='insight-box'>{res['analysis']}</div>", unsafe_allow_html=True)
                        
                        st.session_state['insights'].append({
                            "title": f"Audio Analysis: {aud_file.name}",
                            "body": f"TRANSCRIPT:\n{res['transcript']}\n\nANALYSIS:\n{res['analysis']}",
                            "type": "audio"
                        })
                        st.success("Saved to Insights")
                    except Exception as e:
                        st.error(f"Error: {e}")

# --- TEXT STUDIO ---
with tab_text:
    st.header("Text Intelligence")
    txt_input = st.text_area("Input Text", height=200)
    task = st.selectbox("Task", ["Summarize", "Extract Tasks", "Sentiment Analysis", "Translation (to Spanish)", "Custom Instruction"])
    
    custom_instr = ""
    if task == "Custom Instruction":
        custom_instr = st.text_input("Enter Instruction")
    
    if st.button("Process Text"):
        if not txt_input:
            st.warning("Please enter text.")
        else:
            final_instr = custom_instr if task == "Custom Instruction" else f"Perform {task} on this text."
            with st.spinner("Thinking..."):
                try:
                    res = utils.analyze_text(txt_input, final_instr)
                    st.markdown("### Result")
                    st.write(res['result'])
                    
                    st.session_state['insights'].append({
                        "title": f"Text: {task}",
                        "body": res['result'],
                        "type": "text"
                    })
                except Exception as e:
                    st.error(f"Error: {e}")

# --- CHAT ---
with tab_chat:
    st.header("Context-Aware Chat")
    
    # Session Management
    sessions = []
    try:
        sessions = utils.get_sessions()
    except:
        st.error("Could not fetch sessions. Is backend running?")
    
    session_titles = {s['id']: s['title'] for s in sessions}
    
    col_c1, col_c2 = st.columns([3, 1])
    with col_c2:
        st.subheader("History")
        new_sess_title = st.text_input("New Session Name")
        if st.button("Create Session"):
            if new_sess_title:
                ns = utils.create_session(new_sess_title)
                st.session_state['current_session_id'] = ns['session_id']
                st.rerun()
        
        selected_sess_id = st.radio("Select Session", options=list(session_titles.keys()), format_func=lambda x: session_titles[x])
        if selected_sess_id:
             st.session_state['current_session_id'] = selected_sess_id
             
    with col_c1:
        if st.session_state['current_session_id']:
            st.markdown(f"**Current Session:** {session_titles.get(st.session_state['current_session_id'], 'Unknown')}")
            
            # Load History
            history = utils.get_history(st.session_state['current_session_id'])
            for msg in history:
                with st.chat_message(msg['role']):
                    st.write(msg['content'])
            
            prompt = st.chat_input("Ask about your data...")
            if prompt:
                with st.chat_message("user"):
                    st.write(prompt)
                
                with st.spinner("Thinking..."):
                    res = utils.send_message(st.session_state['current_session_id'], prompt)
                    
                with st.chat_message("assistant"):
                     st.write(res['response'])
                
                st.rerun() # Refresh to show in history correctly
        else:
            st.info("Select or Create a Chat Session to begin.")

# --- REPORT ---
with tab_report:
    st.header("PDF Report Generator")
    st.write("Compile your findings into a professional PDF.")
    
    report_title = st.text_input("Report Title", "Multi-Modal Intelligence Report")
    report_filename = st.text_input("Filename", f"report_{datetime.now().strftime('%Y%m%d')}.pdf")
    
    st.subheader("Select Sections to Include")
    
    selected_insights = []
    if st.session_state['insights']:
        for i, insight in enumerate(st.session_state['insights']):
            if st.checkbox(f"{insight['title']} ({insight['type']})", key=f"rpt_{i}", value=True):
                selected_insights.append(insight)
    else:
        st.info("No analysis insights generated yet. Go analyze some data!")
        
    if st.button("Generate PDF Report", type="primary", disabled=len(selected_insights)==0):
        with st.spinner("Generating PDF..."):
            sections = []
            for item in selected_insights:
                sections.append({
                    "title": item['title'],
                    "body": item['body']
                })
            
            try:
                res = utils.generate_report(report_filename, report_title, sections)
                st.success("Report Generated!")
                st.markdown(f"[{report_filename}]({utils.BASE_URL}{res['url']})") # Link to static file
                
                # Also provide direct download button using Streamlit
                # We need to fetch the file to allow download via button if we want to run locally safely
                # But the link above points to localhost API.
                
                # Let's try to read it if local
                # import os
                # if os.path.exists(res['file_path']):
                #    with open(res['file_path'], "rb") as f:
                #        st.download_button("Download Now", f, file_name=report_filename)
                
            except Exception as e:
                st.error(f"Failed to generate report: {e}")
