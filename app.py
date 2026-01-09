import streamlit as st
import google.generativeai as genai
from duckduckgo_search import DDGS
import time

# --- Page Configuration ---
st.set_page_config(
    page_title="Pharma Research Agent",
    page_icon="💊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Custom CSS for Professional UI ---
st.markdown("""
<style>
    .main {
        background-color: #f8f9fa;
    }
    .stButton>button {
        width: 100%;
        border-radius: 5px;
        height: 3em;
        background-color: #4CAF50;
        color: white;
        font-weight: bold;
    }
    .stTextInput>div>div>input {
        border-radius: 5px;
    }
    .research-card {
        background-color: white;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        margin-bottom: 20px;
    }
    .sidebar-header {
        font-size: 1.2rem;
        font-weight: bold;
        color: #333;
        margin-bottom: 1rem;
    }
</style>
""", unsafe_allow_html=True)

# --- Logic: Search & Summarize ---
def research_drug(drug_name, api_key, model_name):
    """
    Searches DuckDuckGo for the drug and uses Gemini to summarize.
    """
    if not api_key or "YOUR_GEMINI_API_KEY" in api_key:
        return "⚠️ Please configure your Google Gemini API Key in .streamlit/secrets.toml or the sidebar."

    try:
        # 1. Search Web
        with st.spinner(f"🔍 Searching web for '{drug_name}'..."):
            with DDGS() as ddgs:
                results = list(ddgs.text(f"{drug_name} drug medical overview side effects mechanism", max_results=5))
            
            if not results:
                return "No search results found. Please check the drug name."
            
            search_context = "\n\n".join([f"Source: {r['title']}\nSnippet: {r['body']}\nLink: {r['href']}" for r in results])

        # 2. Summarize with Gemini
        with st.spinner(f"🧠 Analyzing data with Gemini..."):
            genai.configure(api_key=api_key)
            model = genai.GenerativeModel(model_name)
            
            prompt = f"""
            You are an expert pharmaceutical researcher. 
            Detailed Research Request for Drug: {drug_name}

            Using the following web search results, provide a professional and comprehensive summary.
            
            Web Search Data:
            {search_context}

            Structure your response as follows:
            1. **Overview**: What is {drug_name} and what is it primarily used for?
            2. **Mechanism of Action**: Briefly how does it work?
            3. **Key Side Effects & Warnings**: Important safety information.
            4. **Recent News/Updates**: Any recent developments found in the snippets (if any).
            5. **References**: List the source titles and links provided.

            Keep it concise but informative for a medical professional or researcher.
            """
            
            response = model.generate_content(prompt)
            return response.text

    except Exception as e:
        return f"An error occurred: {str(e)}"

# --- Sidebar: History & Config ---
st.sidebar.markdown('<div class="sidebar-header">⚙️ Configuration</div>', unsafe_allow_html=True)

# Model Selection
model_options = [
    "gemini-2.0-flash-exp",
    "gemini-2.0-flash",
    "gemini-2.5-flash",
    "gemini-flash-latest",
    "gemini-1.5-flash-latest" # Fallback mapping
]
selected_model = st.sidebar.selectbox("Select AI Model", model_options, index=0)

st.sidebar.markdown('<div class="sidebar-header">🔬 Research History</div>', unsafe_allow_html=True)

if "history" not in st.session_state:
    st.session_state.history = []

# Display history in reverse order
for i, item in enumerate(reversed(st.session_state.history)):
    with st.sidebar.expander(f"📅 {item['timestamp']} - {item['drug']}"):
        st.write(item['summary'][:150] + "...")

st.sidebar.divider()
st.sidebar.info("Built with Streamlit & Gemini 1.5 Flash")

# --- Main Interface ---
st.title("💊 AutoPharma AI Research Agent")
st.markdown("### Intelligent Drug Information Summarizer")

col1, col2 = st.columns([3, 1])
with col1:
    drug_input = st.text_input("Enter Drug Name", placeholder="e.g., Atorvastatin, Pembrolizumab...")

with col2:
    st.write("") # Spacing
    st.write("") 
    research_btn = st.button("🚀 Start Research")

# API Key Handling
try:
    api_key = st.secrets["GOOGLE_API_KEY"]
except (FileNotFoundError, KeyError):
    api_key = st.sidebar.text_input("Enter Google API Key", type="password")
    if not api_key:
        st.warning("Please add your GOOGLE_API_KEY to .streamlit/secrets.toml or the sidebar to proceed.")

# --- Execution ---
if research_btn and drug_input and api_key:
    summary = research_drug(drug_input, api_key, selected_model)
    
    # Store in history
    timestamp = time.strftime("%H:%M:%S")
    st.session_state.history.append({"drug": drug_input, "summary": summary, "timestamp": timestamp})
    
    # Display Result
    st.markdown("---")
    st.markdown(f"## 📋 Research Report: {drug_input}")
    
    with st.container():
        st.markdown('<div class="research-card">', unsafe_allow_html=True)
        st.markdown(summary)
        st.markdown('</div>', unsafe_allow_html=True)

elif research_btn and not drug_input:
    st.error("Please enter a drug name.")
