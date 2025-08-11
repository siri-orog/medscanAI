
import streamlit as st
import easyocr
import pandas as pd
import cv2
import tempfile
import os

# Load drug database (example structure)
@st.cache_data
def load_drug_database():
    return pd.DataFrame({
        'Drug Name': ['Paracetamol', 'Ibuprofen', 'Aspirin', 'Amoxicillin', 'Ciprofloxacin'],
        'Use': [
            'Pain reliever / Fever reducer',
            'Anti-inflammatory / Pain reliever',
            'Blood thinner / Pain reliever',
            'Antibiotic',
            'Antibiotic'
        ],
        'Side Effects': [
            'Nausea, allergic reactions',
            'Stomach pain, dizziness',
            'Bleeding, gastric issues',
            'Diarrhea, rash, nausea',
            'Tendon rupture, nausea, dizziness'
        ],
        'Interactions': [
            'Alcohol, warfarin',
            'Aspirin, alcohol, BP meds',
            'Warfarin, ibuprofen',
            'Birth control, alcohol',
            'Antacids, theophylline'
        ]
    })

drug_data = load_drug_database()

# Title
st.set_page_config(page_title="MedScanAI - Prescription Scanner", layout="centered")
st.title("💊 MedScanAI - Smart Prescription Scanner")
st.write("Upload a prescription image to extract drug names and receive safety alerts.")

# Upload image
uploaded_file = st.file_uploader("Upload a prescription image", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    # Save uploaded image to a temporary file
    temp_file = tempfile.NamedTemporaryFile(delete=False)
    temp_file.write(uploaded_file.read())
    temp_file.close()
    img_path = temp_file.name

    # Display uploaded image
    st.image(img_path, caption="Uploaded Prescription", use_column_width=True)

    # OCR
    reader = easyocr.Reader(['en'])
    result = reader.readtext(img_path, detail=0)
    extracted_text = " ".join(result).lower()
    st.subheader("📄 Extracted Text:")
    st.write(extracted_text)

    # Match drugs
    st.subheader("💡 Identified Drugs and Info:")
    found_drugs = []
    for index, row in drug_data.iterrows():
        if row['Drug Name'].lower() in extracted_text:
            found_drugs.append(row)

    if found_drugs:
        for drug in found_drugs:
            st.markdown(f"### ✅ {drug['Drug Name']}")
            st.markdown(f"**Use:** {drug['Use']}")
            st.markdown(f"**Side Effects:** {drug['Side Effects']}")
            st.markdown(f"**Interactions:** {drug['Interactions']}")
    else:
        st.warning("No known drugs found in the text.")

    # Remove temp image file
    os.remove(img_path)
