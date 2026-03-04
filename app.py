import streamlit as st
import requests
import pandas as pd
import urllib.parse

# --- SUPER PROJECT: ASTRAEA GUARD ---
st.set_page_config(page_title="Astraea Guard: AI Compliance", layout="wide")

st.title("🛡️ Astraea Guard")
st.subheader("Universal AI Ethics & Compliance Architect")

# --- STEP 1: AI LOGIC (HuggingFace Integration) ---
HF_API_URL = "https://api-inference.huggingface.co/models/facebook/bart-large-cnn"
# Note: In a real deployment, use st.secrets for the token.
HF_TOKEN = st.text_input("Enter your HuggingFace Token to Activate:", type="password")

def analyze_compliance(text):
    headers = {"Authorization": f"Bearer {HF_TOKEN}"}
    payload = {"inputs": f"Analyze this AI project for ethical compliance and risks: {text}"}
    response = requests.post(HF_API_URL, headers=headers, json=payload)
    return response.json()

# --- STEP 2: USER INTERFACE (Streamlit) ---
col1, col2 = st.columns([1, 1])

with col1:
    st.info("Input your AI System Description or Code below.")
    user_input = st.text_area("AI Project Scope:", height=200, placeholder="e.g., A facial recognition system for retail stores...")
    
    if st.button("Generate Compliance Audit"):
        if not HF_TOKEN:
            st.warning("Please enter your HuggingFace Token!")
        else:
            with st.spinner("Astraea is auditing..."):
                result = analyze_compliance(user_input)
                st.session_state['audit'] = result[0]['summary_text']

# --- STEP 3: THE REPORT & LINKEDIN INTEGRATION ---
with col2:
    if 'audit' in st.session_state:
        st.success("✅ Audit Complete")
        st.write(st.session_state['audit'])
        
        # Super Feature: One-Click LinkedIn Share
        audit_text = f"I just generated an AI Compliance Report using Astraea Guard! Result: {st.session_state['audit'][:100]}..."
        encoded_text = urllib.parse.quote(audit_text)
        linkedin_url = f"https://www.linkedin.com/sharing/share-offsite/?text={encoded_text}"
        
        st.markdown(f'''
            <a href="{linkedin_url}" target="_blank">
                <button style="background-color: #0077b5; color: white; border: none; padding: 10px 20px; border-radius: 5px; cursor: pointer;">
                    📢 Share Audit to LinkedIn
                </button>
            </a>
        ''', unsafe_allow_index=True)
