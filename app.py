import streamlit as st
import requests
import urllib.parse
import time

st.set_page_config(page_title="Astraea Guard", layout="wide", page_icon="🛡️")

# --- 1. SECRETS CHECK ---
try:
    HF_TOKEN = st.secrets["HF_TOKEN"]
except:
    st.error("❌ Key missing in Streamlit Secrets!")
    st.stop()

# --- 2. THE 2026 ROUTER CONFIG ---
API_URL = "https://router.huggingface.co/hf-inference/models/facebook/bart-large-cnn"
headers = {
    "Authorization": f"Bearer {HF_TOKEN}",
    "Content-Type": "application/json",
    "x-wait-for-model": "true" 
}

st.title("🛡️ Astraea Guard")
st.subheader("Universal AI Ethics & Compliance Architect")
st.markdown("---")

user_input = st.text_area("🚀 Describe the AI System Scope for Audit:", height=200, placeholder="Describe the project (e.g., A surveillance system for employee tracking).")

if st.button("🔍 Run Ethical Audit"):
    if user_input:
        with st.spinner("Analyzing Architecture..."):
            payload = {
                "inputs": f"Summarize the ethical risks, bias concerns, and compliance issues for the following AI project: {user_input}",
                "parameters": {"max_length": 150, "min_length": 50}
            }
            
            try:
                response = requests.post(API_URL, headers=headers, json=payload)
                data = response.json()

                if isinstance(data, list) and len(data) > 0:
                    result_text = data[0].get('summary_text', "")
                    
                    # --- THE PROFESSIONAL REPORT LAYOUT ---
                    st.success("✅ Audit Complete!")
                    st.markdown("### 📊 Astraea Compliance Report")
                    st.info(result_text)
                    
                    # LinkedIn Link
                    msg = urllib.parse.quote(f"🛡️ I just generated an AI Compliance Audit using Astraea Guard! \n\nKey Finding: {result_text[:120]}...")
                    st.markdown(f'''<a href="https://www.linkedin.com/sharing/share-offsite/?text={msg}" target="_blank">
                        <button style="background-color: #0077b5; color: white; border: none; padding: 12px 20px; border-radius: 8px; font-weight: bold; cursor: pointer; width: 100%;">
                        📢 Broadcast Audit to LinkedIn</button></a>''', unsafe_allow_html=True)
                else:
                    st.error(f"❌ Router Error: {data}")
            except Exception as e:
                st.error(f"❌ System Error: {e}")
    else:
        st.warning("Please enter a description to begin the audit.")
