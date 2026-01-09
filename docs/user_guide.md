# 📖 AutoPharma AI - User Guide

Welcome to the AutoPharma AI User Guide. This document provides detailed instructions on how to use the research agent effectively.

## 🏁 Getting Started

1.  **Launch the App**: Access the application via your browser (e.g., `http://localhost:8501` or the [Live Demo](https://auto-pharma-ai-madhavmadupu.streamlit.app/)).
2.  **API Key**: If running locally, ensure your Google Gemini API key is configured in `.streamlit/secrets.toml`. If the app prompts you, you can also enter it in the sidebar.

## 🧪 Performing a Search

The core feature of AutoPharma AI is generating research summaries for specific drugs.

### Steps:
1.  **Enter Drug Name**: In the main text input field labeled **"Enter Drug Name"**, type the generic or brand name of the medication (e.g., `Lisinopril`, `Humira`, `Panadol`).
2.  **Select Model (Optional)**:
    -   In the sidebar (left panel), look for the dropdown menu **"Select AI Model"**.
    -   **Default**: `gemini-2.0-flash-exp` (Recommended for free tier).
    -   **Alternatives**: If you encounter quota limits, try `gemini-2.0-flash` or `gemini-2.5-flash`.
3.  **Start Research**: Click the green **"🚀 Start Research"** button.
4.  **Wait for Processing**: The app will display a spinner while it:
    -   🔍 Searches the web via DuckDuckGo.
    -   🧠 Analyzes the results with Google Gemini.

## 📋 The Research Report

Once processing is complete, a structured report appears containing:
-   **Overview**: What the drug is and its primary uses.
-   **Mechanism of Action**: How the drug works in the body.
-   **Key Side Effects & Warnings**: Crucial safety information.
-   **Recent News/Updates**: Any latest findings from the web search.
-   **References**: Links to the sources used for the summary.

## 🕒 Research History

The sidebar automatically saves your session's search history.
-   **View History**: Expand any item in the **"🔬 Research History"** section to see a snippet of previous reports.
-   **Note**: History is cleared when you refresh the page.

## ❓ Troubleshooting

| Issue | Possible Cause | Solution |
| :--- | :--- | :--- |
| **"Quota Exceeded" (429 Error)** | You hit the rate limit for the selected model. | Switch to a different model in the sidebar (e.g., from `gemini-2.0-flash` to `gemini-1.5-flash-latest`). |
| **"No search results found"** | The drug name might be misspelled. | Check the spelling and try again. |
| **"Please configure your... API Key"** | API Key is missing or invalid. | valid key in `.streamlit/secrets.toml` or the sidebar input. |

---
*For technical details, please refer to the [Developer Guide](developer_guide.md).*
