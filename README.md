# 💊 AutoPharma AI Research Agent

![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=Streamlit&logoColor=white)
![Gemini](https://img.shields.io/badge/Google%20Gemini-8E75B2?style=for-the-badge&logo=google%20gemini&logoColor=white)
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)

**AutoPharma AI** is an intelligent drug research assistant powered by **Google Gemini 2.0** and **DuckDuckGo Search**. It automates the process of gathering medical information, providing structured, professional summaries for researchers and healthcare professionals.

🚀 **Live Demo:** [Check out the App](https://auto-pharma-ai-madhavmadupu.streamlit.app/)

## ✨ Features

-   **🔍 Real-time Web Search**: Fetches the latest drug information, side effects, and news using DuckDuckGo.
-   **🧠 AI Powered Summaries**: Uses **Gemini 2.0 Flash** to synthesize disparate search results into a clean, readable report.
-   **📝 Research History**: Automatically tracks your search queries in the sidebar for easy reference.
-   **⚙️ Model Selection**: Switch between different Gemini models (e.g., `gemini-2.0-flash-exp`, `gemini-2.0-flash`) directly from the UI.
-   **🔒 Secure**: API keys are handled securely via Streamlit secrets.

## 🚀 Getting Started

### Prerequisites

-   Python 3.8+
-   A Google Gemini API Key ([Get one here](https://aistudio.google.com/app/apikey))

### Installation

1.  **Clone the repository** (if applicable) or download the source code.

2.  **Create a virtual environment**:
    ```bash
    python -m venv venv
    # Windows
    .\venv\Scripts\activate
    # Mac/Linux
    source venv/bin/activate
    ```

3.  **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

4.  **Configure API Key**:
    Create a file named `.streamlit/secrets.toml` in the project root:
    ```toml
    # .streamlit/secrets.toml
    GOOGLE_API_KEY = "YOUR_API_KEY_HERE"
    ```

### Running the App

```bash
streamlit run app.py
```
The application will launch in your default web browser at `http://localhost:8501`.

## 🛠️ Usage

1.  **Enter Drug Name**: Type the name of a drug (e.g., *Metformin*, *Atorvastatin*) in the main input field.
2.  **Select Model**: (Optional) Choose a specific Gemini model from the sidebar.
3.  **Start Research**: Click the "Start Research" button.
4.  **Review Report**: Read the generated summary covering overview, mechanism of action, side effects, and recent news.
5.  **Check History**: Previous searches are saved in the sidebar for quick access.

## 📦 Tech Stack

-   **Frontend**: [Streamlit](https://streamlit.io/)
-   **LLM**: [Google Gemini API](https://ai.google.dev/) (`google-generativeai`)
-   **Search**: [DuckDuckGo Search](https://pypi.org/project/duckduckgo-search/) (`duckduckgo-search`)

## 📄 License

This project is open-source and available under the [MIT License](LICENSE).
