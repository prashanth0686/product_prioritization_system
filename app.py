import streamlit as st
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from google import genai
import pandas as pd
import json
import re
import os
from dotenv import load_dotenv

# --- 1. CONFIGURATION ---
load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY")

st.set_page_config(page_title="Final AI PM Agent", page_icon="🚀")
st.title("🚀 Final AI Product Prioritization Agent")

if st.button("Generate Prioritized Roadmap"):
    if not API_KEY:
        st.error("API Key not found in .env file.")
        st.stop()

    with st.spinner("Calculating RICE scores..."):
        try:
            # A. Sheets Connection
            scope = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]
            creds = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", scope)
            gc = gspread.authorize(creds)
            spreadsheet = gc.open("Python Google Sheets Integration")
            input_sheet = spreadsheet.sheet1
            
            # B. Read and Sanitize Data
            df_raw = pd.DataFrame(input_sheet.get_all_records())
            df_clean = df_raw.fillna("N/A") 
            
            # C. AI Process - FORCING NUMERIC OUTPUT
            client_ai = genai.Client(api_key=API_KEY, http_options={'api_version': 'v1'})
            json_payload = df_clean.to_json(orient='records')
            
            # STRICT PROMPT: Forces numbers for Reach (int), Impact (0.25-3), Conf (0-100), Effort (1-10)
            prompt = (
                "Analyze feedback and cluster into strategic themes. Return ONLY a JSON list of objects. "
                "CRITICAL: Values for 'Reach', 'Impact', 'Confidence', and 'Effort' MUST be RAW NUMBERS only. "
                "Example format: {'Theme': 'UI Fix', 'Reach': 500, 'Impact': 2, 'Confidence': 80, 'Effort': 3}. "
                f"Data: {json_payload}"
            )
            
            # Using your confirmed working model
            response = client_ai.models.generate_content(model="gemini-2.5-flash", contents=prompt)
            
            # D. Robust Parsing and Score Calculation
            clean_text = re.search(r'\[.*\]', response.text, re.DOTALL).group(0)
            results_df = pd.DataFrame(json.loads(clean_text))
            
            # Convert to numeric, stripping common non-numeric chars
            for col in ['Reach', 'Impact', 'Confidence', 'Effort']:
                results_df[col] = pd.to_numeric(
                    results_df[col].astype(str).str.replace(r'[%,]', '', regex=True), 
                    errors='coerce'
                ).fillna(0)

            # RICE Formula implementation
            # Score = (Reach * Impact * (Confidence/100)) / Effort
            results_df['RICE_Score'] = (
                results_df['Reach'] * results_df['Impact'] * (results_df['Confidence'] / 100)
            ) / results_df['Effort'].replace(0, 1) # Safety check for 0 effort
            
            results_df = results_df.sort_values(by='RICE_Score', ascending=False)

            # E. Output Sync
            try:
                output_tab = spreadsheet.worksheet("Roadmap Output")
            except:
                output_tab = spreadsheet.add_worksheet(title="Roadmap Output", rows="100", cols="20")
            
            output_tab.clear()
            output_tab.update([results_df.columns.values.tolist()] + results_df.values.tolist())
            
            st.success("✅ Roadmap Calculated and Synced!")
            st.dataframe(results_df) # Show results in the app for verification
            st.balloons()

        except Exception as e:
            st.error(f"Execution Error: {e}")