import streamlit as st
import requests
import urllib.parse
import time

st.set_page_config(page_title="Astraea Guard", layout="wide", page_icon="🛡️")

# --- 1. SECRETS CHECK ---
try:
    HF_TOKEN = st.secrets["HF_TOKEN"]
except:
    st.error("❌ Key missing in Streamlit Secrets! Check Step 1 again.")
    st.stop()

# --- 2. THE NEW 2026 ROUTER CONFIG ---
API_URL = "https://router.huggingface.co/hf-inference/models/facebook/bart-large-cnn"

# We move "wait-for-model" to the HEADERS to avoid the "model_kwargs" error
headers = {
    "Authorization": f"Bearer {HF_TOKEN}",
    "Content-Type": "application/json",
    "x-wait-for-model": "true" 
}

st.title("🛡️ Astraea Guard")
st.subheader("Universal AI Ethics & Compliance Architect")
st.divider()

user_input = st.text_area("Describe the AI System Scope:", height=200, placeholder="Describe your AI project here...")

if st.button("🚀 Run Ethical Audit"):
    if user_input:
        with st.spinner("Astraea is consulting the global AI router..."):
            # Clean payload without the 'wait_for_model' conflict
            payload = {
                "inputs": f"Summarize the ethical and compliance risks for: {user_input}",
                "parameters": {"max_length": 150}
            }
            
            try:
                response = requests.post(API_URL, headers=headers, json=payload)
                data = response.json()

                # Success logic
                if isinstance(data, list) and len(data) > 0:
                    result_text = data[0].get('summary_text', "No summary returned.")
                    st.success("✅ Audit Complete!")
                    st.write(result_text)
                    
                    # LinkedIn Link
                    msg = urllib.parse.quote(f"Astraea Guard Audit: {result_text[:120]}...")
                    st.markdown(f'''<a href="https://www.linkedin.com/sharing/share-offsite/?text={msg}" target="_blank">
                        <button style="background-color: #0077b5; color: white; border: none; padding: 12px 20px; border-radius: 8px; font-weight: bold; cursor: pointer;">
                        📢 Post Audit to LinkedIn</button></a>''', unsafe_allow_html=True)
                
                # If there is still an error, show exactly what it is
                else:
                    st.error(f"❌ Router Error: {data}")
                    
            except Exception as e:
                st.error(f"❌ System Error: {e}")
    else:
        st.warning("Please enter a description.")
