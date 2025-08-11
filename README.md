# medscanAI
# 🤖 MedScanAI – AI Health & Prescription Assistant

MedScanAI is a Python + Streamlit application that provides detailed information about medicines, including their uses, side effects, and warnings.  
It retrieves real-time drug data from the **FDA Drug Label API** and uses a **local CSV dataset** as a fallback when the API is unavailable.

### Features
- Search any drug name and get instant results.
- Real-time FDA API integration.
- Offline mode using local dataset.
- Simple and interactive web interface.

### Setup
1. Install dependencies:
   ```bash
   pip install -r requirements.txt
streamlit run medscanai_assistant_chat.py
Dataset
Online: FDA Drug Label API

Offline: drug_data_clean_100rows.csv with Indian drug samples.

### How It Works
User enters a drug name.
The app first queries the FDA API.
If API fails or no result found → it uses the local CSV dataset.
Displays the results clearly.

### Future Enhancements
OCR + NLP for multi-drug prescriptions
Drug–drug interaction checker
Integration with India’s CDSCO database
Mobile app version
