# 🚀 AI Product Prioritization Agent

An agentic system that clusters raw product feedback into strategic themes and calculates **RICE scores** (Reach, Impact, Confidence, Effort) using **Gemini 2.5 Flash**.

## ✨ Features
* **Automated Clustering**: Groups unstructured user feedback into themes.
* **RICE Prioritization**: Mathematical ranking to remove human bias.
* **Google Sheets Sync**: Fetches raw data and pushes results back in real-time.

## 🛠️ Setup Instructions
1. **Clone the Repo**: `git clone https://github.com/yourusername/repo-name.git`
2. **Install Dependencies**: `py -m pip install -r requirements.txt`
3. **Configure Secrets**: 
   * Add your `GEMINI_API_KEY` to a `.env` file.
   * Add your Google Service Account `credentials.json` to the root folder.
4. **Run the App**: `py -m streamlit run app.py`

## 📊 How it Works
The agent uses a Python bridge to communicate between the **Google Sheets API** and **Google GenAI SDK**. It ensures data integrity by sanitizing `NaN` values before processing.