# 👨‍💻 AutoPharma AI - Developer Guide

This guide is for developers looking to understand, modify, or deploy the AutoPharma AI application.

## 🏗️ Architecture

The application is built using a simple 3-tier logic flow:

1.  **Frontend (UI)**: Built with **Streamlit**. Handles user input, displays results, and manages session state.
2.  **Data Acquisition**: Uses `duckduckgo-search` to fetch real-time search results (HTML/Text snippets) from the web.
3.  **Intelligence Layer**: Uses **Google Gemini API** (`google-generativeai`) to process the raw search data and generate a structured markdown summary.

**File Structure:**
```
auto-pharma-ai/
├── .streamlit/
│   └── secrets.toml      # API Keys (Not committed)
├── docs/                 # Documentation
│   ├── user_guide.md
│   └── developer_guide.md
├── venv/                 # Virtual Environment
├── app.py                # Main Application Entry Point
├── requirements.txt      # Python Dependencies
└── README.md             # Project Overview
```

## ⚙️ Development Setup

1.  **Environment**:
    ```bash
    python -m venv venv
    venv\Scripts\activate
    pip install -r requirements.txt
    ```

2.  **Configuration**:
    Ensure `.streamlit/secrets.toml` exists:
    ```toml
    GOOGLE_API_KEY = "YOUR_KEY"
    ```

3.  **Run Locally**:
    ```bash
    streamlit run app.py
    ```

## 🧩 Key Functions in `app.py`

-   **`research_drug(drug_name, api_key, model_name)`**:
    -   **Inputs**: Drug name, API Key, Model string.
    -   **Steps**:
        1.  Calls `DDGS().text()` to get search results.
        2.  Formats results into a "Search Context".
        3.  Sends context + prompt to `genai.GenerativeModel`.
    -   **Returns**: Markdown string of the summary.

## 🚀 Deployment

The app is optimized for **Streamlit Cloud**.

1.  Push code to GitHub.
2.  Connect repository to Streamlit Cloud.
3.  **Crucial**: Add your `GOOGLE_API_KEY` in the Streamlit Cloud "Secrets" management section (found in App Settings).

## 🤝 Contributing

-   **Adding Models**: Update the `model_options` list in `app.py`.
-   **Changing Prompts**: Modify the `prompt` f-string in `research_drug` to change the output structure or persona.
