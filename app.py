import streamlit as st
import requests
import urllib.parse
import time

# ASTRAEA GUARD: THE FINAL MASTER CODE
st.set_page_config(page_title="Astraea Guard", layout="wide", page_icon="🛡️")

# 1. ATTEMPTING TO ACCESS THE BRAIN KEY
try:
    # This looks inside the Streamlit Secrets box you just filled in Step 1
    HF_TOKEN = st.secrets["HF_TOKEN"]
except Exception:
    st.error("❌ ARCHITECT ERROR: The Secret Key is missing or incorrectly formatted in Streamlit Secrets!")
    st.stop()

# 2. DEFINING THE AI BRAIN CONNECTION
API_URL = "https://api-inference.huggingface.co/models/facebook/bart-large-cnn"
headers = {"Authorization": f"Bearer {HF_TOKEN}"}

def query_brain(payload):
    response = requests.post(API_URL, headers=headers, json=payload)
    return response.json()

# 3. THE VISUAL DASHBOARD
st.title("🛡️ Astraea Guard")
st.subheader("Universal AI Ethics & Compliance Architect")
st.divider()

col1, col2 = st.columns([1, 1])

with col1:
    st.markdown("### 📝 Audit Input")
    user_input = st.text_area("Describe the AI System Scope:", height=250, 
                              placeholder="e.g., A surveillance system using facial recognition.")
    
    if st.button("🚀 Run Ethical Audit"):
        if user_input:
            with st.spinner("Astraea is calculating ethical risks..."):
                data = query_brain({"inputs": f"Summarize the ethical risks for this AI project: {user_input}"})
                
                # Check if the brain is warming up
                if isinstance(data, dict) and "estimated_time" in data:
                    wait_time = int(data["estimated_time"])
                    st.info(f"🔄 The AI Brain is warming up... please wait {wait_time} seconds.")
                    time.sleep(wait_time)
                    data = query_brain({"inputs": f"Summarize the ethical risks: {user_input}"})
                
                # Success display
                if isinstance(data, list) and len(data) > 0:
                    st.session_state['result'] = data[0]['summary_text']
                else:
                    st.error("⚠️ Connection failed. Wait 30 seconds and try again.")
        else:
            st.warning("Please enter a description first!")

with col2:
    if 'result' in st.session_state:
        st.markdown("### ✅ Compliance Report")
        st.success(st.session_state['result'])
        
        # LINKEDIN INTEGRATION
        encoded_msg = urllib.parse.quote(f"I just deployed Astraea Guard! My AI Audit Result: {st.session_state['result'][:150]}...")
        li_url = f"https://www.linkedin.com/sharing/share-offsite/?text={encoded_msg}"
        
        st.markdown(f'''
            <a href="{li_url}" target="_blank">
                <button style="background-color: #0077b5; color: white; border: none; padding: 15px; border-radius: 10px; width: 100%; font-weight: bold; cursor: pointer;">
                    📢 Share to LinkedIn
                </button>
            </a>
        ''', unsafe_allow_html=True)
