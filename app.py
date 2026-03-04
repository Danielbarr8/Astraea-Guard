import streamlit as st
import requests
import pandas as pd
import urllib.parse

# --- SUPER PROJECT: ASTRAEA GUARD ---
# This sets up the browser tab and layout
st.set_page_config(page_title="Astraea Guard: AI Compliance", layout="wide", page_icon="🛡️")

st.title("🛡️ Astraea Guard")
st.subheader("Universal AI Ethics & Compliance Architect")
st.markdown("---")

# --- STEP 1: AI LOGIC (HuggingFace Integration) ---
# This line connects to the 'Safe' (Secrets) you built in Streamlit
try:
    HF_TOKEN = st.secrets["HF_TOKEN"]
except:
    st.error("Missing HF_TOKEN in Streamlit Secrets!")
    st.stop()

HF_API_URL = "https://api-inference.huggingface.co/models/facebook/bart-large-cnn"

def analyze_compliance(text):
    headers = {"Authorization": f"Bearer {HF_TOKEN}"}
    payload = {"inputs": f"Analyze this AI project for ethical compliance and risks: {text}"}
    response = requests.post(HF_API_URL, headers=headers, json=payload)
    return response.json()

# --- STEP 2: USER INTERFACE (Streamlit) ---
col1, col2 = st.columns([1, 1])

with col1:
    st.info("### 📝 Audit Scope")
    st.write("Input your AI System Description or Code below for a deep ethical analysis.")
    user_input = st.text_area("", height=250, placeholder="e.g., A system using biometric data to predict credit scores...")
    
    if st.button("🚀 Generate Compliance Audit"):
        with st.spinner("Astraea is auditing the architecture..."):
            try:
                result = analyze_compliance(user_input)
                # Store the result so it stays on the screen
                st.session_state['audit'] = result[0]['summary_text']
            except Exception as e:
                st.error(f"Brain connection failed: {e}")

# --- STEP 3: THE REPORT & LINKEDIN INTEGRATION ---
with col2:
    if 'audit' in st.session_state:
        st.success("### ✅ Audit Complete")
        st.write(st.session_state['audit'])
        
        # Super Feature: One-Click LinkedIn Share
        # We prepare the text for your professional network
        audit_summary = st.session_state['audit'][:150]
        share_text = f"I just deployed Astraea Guard, my AI Compliance Architect! Audit result: {audit_summary}..."
        encoded_text = urllib.parse.quote(share_text)
        linkedin_url = f"https://www.linkedin.com/sharing/share-offsite/?text={encoded_text}"
        
        st.markdown(f'''
            <div style="margin-top: 20px;">
                <p><strong>Ready to share your expertise?</strong></p>
                <a href="{linkedin_url}" target="_blank">
                    <button style="background-color: #0077b5; color: white; border: none; padding: 12px 24px; border-radius: 8px; font-weight: bold; cursor: pointer; width: 100%;">
                        📢 Share Audit to LinkedIn
                    </button>
                </a>
            </div>
        ''', unsafe_allow_html=True)
