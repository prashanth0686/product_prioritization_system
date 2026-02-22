# 🚀 Technical Documentation: AI-Driven Product Prioritization Agent

## 1. Executive Summary

The AI Product Prioritization Agent is an autonomous system designed to transform raw, unstructured user feedback into a data-driven product roadmap.  
By leveraging Gemini 2.0 Flash, the agent categorizes feedback into logical themes and assigns objective RICE scores, eliminating manual analysis and subjective bias in product planning.[web:6][web:8][web:1]

## 2. Implementation Details

### Tech Stack

- Interface: Streamlit (Web UI)
- Orchestration: Python 3.10+
- LLM Engine: Google Gemini 2.0 Flash (via google-genai SDK)[web:6][web:12]
- Data Storage: Google Sheets API (gspread)
- Authentication: Google Service Account (OAuth 2.0)

### System Architecture

- Ingestion: The agent pulls raw data from the "Input" tab of a Google Sheet.
- Sanitization: Data is cleaned (NaN/null removal) to ensure JSON compatibility.
- Intelligence Layer: The LLM processes the feedback to derive themes and estimates.[web:6][web:8]
- Processing: Python calculates the final RICE scores and sorts the results.[web:1][web:5]
- Output: Results are pushed to a "Roadmap Output" tab and made available for CSV download.

## 3. The Agentic Approach

### What makes it "Agentic"?

Unlike a simple script, this implementation follows an Agentic Workflow:

- Autonomy: The agent is given a high-level goal ("Prioritize this feedback") and decides how to cluster disparate comments into cohesive "Themes" without being told what the themes are in advance.[web:6][web:8]
- Reasoning: It uses zero-shot reasoning to evaluate qualitative feedback (for example, "The app is slow") and translate it into quantitative estimates (for example, Reach: 80, Impact: 2).[web:6][web:8]
- Tool Use: The agent interacts with external environments (Google Sheets) to read state and write results, bridging the gap between "thinking" and "doing".[web:6][web:12]

### Why use an LLM?

- Semantic Clustering: Traditional keyword matching misses the point; an LLM understands that "Login is broken" and "Can't get past the sign-in screen" are the same theme.[web:6][web:8]
- Bias Mitigation: The LLM acts as an objective third party, assigning scores based on feedback content rather than internal team politics or "loudest voice" bias.[web:1][web:7]

## 4. RICE Scoring Logic

The agent utilizes the industry-standard RICE Framework to calculate priority:[web:1][web:5][web:7]

\[
RICE\ Score = \frac{Reach \times Impact \times Confidence}{Effort}
\]

### Scoring Parameters used by the Agent

| Factor     | Description                      | Agentic Logic                                                                                  |
|-----------|----------------------------------|-----------------------------------------------------------------------------------------------|
| Reach     | How many users this affects      | Estimated based on the frequency and severity of feedback mentions.                           |
| Impact    | Contribution to value            | 3 (Massive), 2 (High), 1 (Medium), 0.5 (Low), 0.25 (Minimal).[web:1][web:5]                  |
| Confidence| Reliability of data              | Defaults to 80% unless feedback is vague or contradictory.[web:1][web:5]                      |
| Effort    | "Person-months" to build         | Estimated based on the technical complexity of the suggested theme.[web:5]                    |

## 5. Sequence of Operations (The LLM Call)

- The LLM is invoked once per generation cycle to minimize token cost and latency.[web:6][web:8]
- Trigger: User clicks "Generate Prioritized Roadmap."
- Context Construction: The Python script assembles a prompt containing the raw feedback and strict JSON formatting instructions.
- The Call: The `generate_content` method sends the data to `gemini-2.0-flash`.[web:6][web:8]
- Parsing: Python intercepts the LLM's response, extracts the JSON array, and performs the mathematical RICE calculations.[web:1][web:5]

## 6. How to Use

- Populate Input: Add raw customer feedback to the first tab of your Google Sheet.
- Run Agent: Launch the Streamlit app and click the action button.
- Review Output: Check the "Roadmap Output" tab in Google Sheets for your sorted, prioritized list of product initiatives.

## Relevant Documentation & Resources

- Intercom's Original RICE Framework[web:1]  
  https://www.intercom.com/blog/rice-simple-prioritization-for-product-managers/

- Google Gemini API Documentation[web:6][web:8]  
  https://ai.google.dev/docs
