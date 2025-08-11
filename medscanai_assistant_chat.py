
import streamlit as st
import pandas as pd
import easyocr
import requests
import tempfile
import os

# Page setup
st.set_page_config(page_title="MedScanAI Assistant", layout="centered")
st.title("🤖 MedScanAI – Your AI Health Assistant")
st.write("👋 Hi! I’m MedScanAI. I can help you understand your prescriptions.")

# Load local drug data
@st.cache_data
def load_drug_data():
    return pd.read_csv("drug_data.csv")

# openFDA API fetch
def get_fda_info(drug_name):
    url = f"https://api.fda.gov/drug/label.json?search=active_ingredient:{drug_name}"
    try:
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            data = response.json()
            if data.get("results"):
                info = data["results"][0]
                return {
                    "use": info.get("indications_and_usage", ["Not available"])[0],
                    "side_effects": info.get("adverse_reactions", ["Not available"])[0],
                    "warnings": info.get("warnings", ["Not available"])[0]
                }
    except:
        pass
    return None


drug_data = load_drug_data()
reader = easyocr.Reader(['en'])

# Chat-like interface
st.markdown("### 💬 How would you like to continue?")
mode = st.radio("", ("📷 Upload a prescription image", "📝 Type medicine names manually"))

text = ""

if mode == "📷 Upload a prescription image":
    st.markdown("**Please upload a clear photo of your prescription.**")
    uploaded_file = st.file_uploader("Choose an image", type=["jpg", "jpeg", "png"])
    if uploaded_file:
        st.image(uploaded_file, caption="📄 Uploaded Prescription", use_column_width=True)
        with st.spinner("🧠 Analyzing image..."):
            temp_file = tempfile.NamedTemporaryFile(delete=False)
            temp_file.write(uploaded_file.read())
            temp_file.close()
            img_path = temp_file.name
            result = reader.readtext(img_path, detail=0)
            text = " ".join(result).lower()
            os.remove(img_path)
        st.success("✅ I’ve extracted the following text:")
        st.write(text)

elif mode == "📝 Type medicine names manually":
    text = st.text_area("Type the medicine names below (separated by commas)", placeholder="e.g., Paracetamol, Ibuprofen").lower()

# Process drug names
if text:
    st.markdown("### 🔍 Let me analyze the medicines for you:")
    found = False
    for drug_name in drug_data['Drug Name'].tolist():
        if drug_name.lower() in text:
            found = True
            st.markdown(f"#### ✅ {drug_name}")
            fda_info = get_fda_info(drug_name.lower())
            if fda_info:
                st.markdown(f"**🧾 Use:** {fda_info['use']}")
                st.markdown(f"**⚠️ Side Effects:** {fda_info['side_effects']}")
                st.markdown(f"**🚨 Warnings:** {fda_info['warnings']}")
            else:
                st.info("ℹ️ Couldn't fetch live data. Here's fallback info:")
                row = drug_data[drug_data['Drug Name'] == drug_name].iloc[0]
                st.markdown(f"**🧾 Use:** {row['Use']}")
                st.markdown(f"**⚠️ Side Effects:** {row['Side Effects']}")
                st.markdown(f"**🚨 Interactions:** {row['Interactions']}")

    if not found:
        st.warning("I couldn’t match any known drug names. Try again with more common names.")
