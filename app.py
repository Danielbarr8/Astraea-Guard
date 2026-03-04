import streamlit as st
import requests
import urllib.parse
import time

st.set_page_config(page_title="Astraea Guard", layout="wide", page_icon="🛡️")

# THE BRAIN KEY
try:
    HF_TOKEN = st.secrets["HF_TOKEN"]
except:
    st.error("❌ Key missing in Streamlit Secrets!")
    st.stop()

# THE BRAIN ADDRESS
API_URL = "https://api-inference.huggingface.co/models/facebook/bart-large-cnn"
headers = {"Authorization": f"Bearer {HF_TOKEN}"}

st.title("🛡️ Astraea Guard")
st.subheader("Universal AI Ethics & Compliance Architect")

user_input = st.text_area("Describe the AI System Scope:", height=200)

if st.button("🚀 Run Ethical Audit"):
    if user_input:
        with st.spinner("Waking up the AI Brain... this can take 20 seconds..."):
            # Try to talk to the brain
            response = requests.post(API_URL, headers=headers, json={"inputs": user_input})
            data = response.json()
            
            # If brain is 'loading', wait 20 seconds and try one more time
            if isinstance(data, dict) and "error" in data:
                st.info("🔄 Brain is still warming up... waiting 20 seconds...")
                time.sleep(20)
                response = requests.post(API_URL, headers=headers, json={"inputs": user_input})
                data = response.json()

            # Show the result
            if isinstance(data, list) and len(data) > 0:
                st.success("✅ Audit Complete!")
                st.write(data[0]['summary_text'])
                
                # LinkedIn Share
                msg = urllib.parse.quote(f"My Astraea Guard Audit: {data[0]['summary_text'][:100]}...")
                st.markdown(f'[📢 Share to LinkedIn](https://www.linkedin.com/sharing/share-offsite/?text={msg})')
            else:
                st.error(f"❌ Brain connection failed. HuggingFace says: {data}")
    else:
        st.warning("Please enter a description.")
