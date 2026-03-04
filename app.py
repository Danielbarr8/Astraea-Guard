import streamlit as st
import requests
import urllib.parse
import time

st.set_page_config(page_title="Astraea Guard", layout="wide", page_icon="🛡️")

# --- SECRETS CHECK ---
try:
    HF_TOKEN = st.secrets["HF_TOKEN"]
except:
    st.error("❌ Key missing in Streamlit Secrets! Check Step 1 again.")
    st.stop()

# --- THE NEW 2026 ROUTER ADDRESS ---
# We switched from api-inference to router.huggingface.co
API_URL = "https://router.huggingface.co/hf-inference/models/facebook/bart-large-cnn"
headers = {"Authorization": f"Bearer {HF_TOKEN}", "Content-Type": "application/json"}

st.title("🛡️ Astraea Guard")
st.subheader("Universal AI Ethics & Compliance Architect")

user_input = st.text_area("Describe the AI System Scope:", height=200, placeholder="e.g., A system that predicts health risks using social media data.")

if st.button("🚀 Run Ethical Audit"):
    if user_input:
        with st.spinner("Connecting to the New AI Router..."):
            # The new Router expects this specific data package
            payload = {
                "inputs": f"Analyze the ethical and compliance risks for this AI project: {user_input}",
                "parameters": {"max_length": 150, "wait_for_model": True}
            }
            
            try:
                response = requests.post(API_URL, headers=headers, json=payload)
                data = response.json()

                # If the brain is loading (Status 503), the code will wait and try again
                if response.status_code == 503:
                    st.info("🔄 The Brain is loading on the new router... waiting 20 seconds.")
                    time.sleep(20)
                    response = requests.post(API_URL, headers=headers, json=payload)
                    data = response.json()

                if isinstance(data, list) and len(data) > 0:
                    result_text = data[0].get('summary_text', "Audit complete, but no text returned.")
                    st.success("✅ Audit Complete!")
                    st.write(result_text)
                    
                    # LinkedIn Link
                    msg = urllib.parse.quote(f"Astraea Guard Audit: {result_text[:100]}...")
                    st.markdown(f'''<a href="https://www.linkedin.com/sharing/share-offsite/?text={msg}" target="_blank">
                        <button style="background-color: #0077b5; color: white; border: none; padding: 10px; border-radius: 5px; cursor: pointer;">
                        📢 Post Audit to LinkedIn</button></a>''', unsafe_allow_html=True)
                else:
                    st.error(f"❌ Connection Issue. The Router said: {data}")
            except Exception as e:
                st.error(f"❌ Critical Error: {e}")
    else:
        st.warning("Please enter a description.")
