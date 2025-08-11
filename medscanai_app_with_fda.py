
import streamlit as st
import easyocr
import pandas as pd
import requests
import tempfile
import os

st.set_page_config(page_title="MedScanAI - Prescription Scanner", layout="centered")
st.title("💊 MedScanAI - Smart Prescription Scanner")
st.write("Upload a prescription image to extract drug names and receive safety alerts.")

# Load local fallback database
@st.cache_data
def load_drug_data():
    return pd.read_csv("drug_data.csv")

# openFDA API call
def get_fda_info(drug_name):
    url = f"https://api.fda.gov/drug/label.json?search=active_ingredient:{drug_name}"
    response = requests.get(url)
    if response.status_code == 200:
        try:
            data = response.json()
            info = data['results'][0]
            return {
                "use": info.get("indications_and_usage", ["N/A"])[0],
                "side_effects": info.get("adverse_reactions", ["N/A"])[0],
                "warnings": info.get("warnings", ["N/A"])[0]
            }
        except Exception:
            return None
    else:
        return None

# Load data and OCR model
drug_data = load_drug_data()
reader = easyocr.Reader(['en'])

# File uploader
uploaded_file = st.file_uploader("Upload a prescription image", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    temp_file = tempfile.NamedTemporaryFile(delete=False)
    temp_file.write(uploaded_file.read())
    temp_file.close()
    img_path = temp_file.name

    st.image(img_path, caption="Uploaded Prescription", use_column_width=True)
    result = reader.readtext(img_path, detail=0)
    text = " ".join(result).lower()
    st.subheader("📄 Extracted Text:")
    st.write(text)

    st.subheader("💊 Identified Drugs:")
    found = False
    for drug_name in drug_data['Drug Name'].tolist():
        if drug_name.lower() in text:
            found = True
            st.markdown(f"### ✅ {drug_name}")

            # Try getting data from openFDA
            info = get_fda_info(drug_name.lower())
            if info:
                st.markdown(f"**Use:** {info['use']}")
                st.markdown(f"**Side Effects:** {info['side_effects']}")
                st.markdown(f"**Warnings:** {info['warnings']}")
            else:
                st.warning("ℹ️ No detailed FDA info available. Showing local data.")
                row = drug_data[drug_data['Drug Name'] == drug_name].iloc[0]
                st.markdown(f"**Use:** {row['Use']}")
                st.markdown(f"**Side Effects:** {row['Side Effects']}")
                st.markdown(f"**Interactions:** {row['Interactions']}")

    if not found:
        st.warning("No known drugs found in the text.")

    os.remove(img_path)
