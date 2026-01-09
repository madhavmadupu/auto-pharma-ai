import streamlit as st
import google.generativeai as genai
from duckduckgo_search import DDGS
from openai import OpenAI
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
def research_drug(drug_name, api_key, provider, model_name):
    """
    Searches DuckDuckGo for the drug and uses the selected AI provider to summarize.
    """
    if not api_key or "YOUR_" in api_key:
        return f"⚠️ Please configure your {provider} API Key in .streamlit/secrets.toml or the sidebar."

    try:
        # 1. Search Web
        with st.spinner(f"🔍 Searching web for '{drug_name}'..."):
            with DDGS() as ddgs:
                results = list(ddgs.text(f"{drug_name} drug medical overview side effects mechanism", max_results=5))
            
            if not results:
                return "No search results found. Please check the drug name."
            
            search_context = "\n\n".join([f"Source: {r['title']}\nSnippet: {r['body']}\nLink: {r['href']}" for r in results])

        # 2. Summarize with AI
        with st.spinner(f"🧠 Analyzing data with {provider}..."):
            
            system_prompt = f"""
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

            if provider == "Google Gemini":
                genai.configure(api_key=api_key)
                model = genai.GenerativeModel(model_name)
                response = model.generate_content(system_prompt)
                return response.text
            
            elif provider == "xAI Grok":
                client = OpenAI(
                    api_key=api_key,
                    base_url="https://api.x.ai/v1",
                )
                response = client.chat.completions.create(
                    model=model_name,
                    messages=[
                        {"role": "system", "content": "You are a helpful pharmaceutical researcher."},
                        {"role": "user", "content": system_prompt},
                    ]
                )
                return response.choices[0].message.content

    except Exception as e:
        return f"An error occurred: {str(e)}"

# --- Sidebar: History & Config ---
st.sidebar.markdown('<div class="sidebar-header">⚙️ Configuration</div>', unsafe_allow_html=True)

# Provider Selection
provider = st.sidebar.radio("Select AI Provider", ["Google Gemini", "xAI Grok"])

# Model Selection
if provider == "Google Gemini":
    model_options = [
        "gemini-2.0-flash-exp",
        "gemini-2.0-flash",
        "gemini-2.5-flash",
        "gemini-flash-latest",
    ]
else: # Grok
    model_options = [
        "grok-2-latest",
        "grok-2-1212",
        "grok-2-mini",
        "grok-beta",
    ]

selected_model = st.sidebar.selectbox("Select Model", model_options, index=0)

# API Key Handling
try:
    if provider == "Google Gemini":
        api_key = st.secrets["GOOGLE_API_KEY"]
    else:
        api_key = st.secrets["XAI_API_KEY"]
except (FileNotFoundError, KeyError):
    api_key_env = "GOOGLE_API_KEY" if provider == "Google Gemini" else "XAI_API_KEY"
    api_key = st.sidebar.text_input(f"Enter {provider} API Key", type="password")
    if not api_key:
        st.warning(f"Please add your {api_key_env} to .streamlit/secrets.toml or the sidebar to proceed.")

st.sidebar.markdown('<div class="sidebar-header">🔬 Research History</div>', unsafe_allow_html=True)

if "history" not in st.session_state:
    st.session_state.history = []

# Display history in reverse order
for i, item in enumerate(reversed(st.session_state.history)):
    with st.sidebar.expander(f"📅 {item['timestamp']} - {item['drug']}"):
        st.write(item['summary'][:150] + "...")

if st.sidebar.button("🗑️ Clear History"):
    st.session_state.history = []
    st.rerun()

st.sidebar.divider()
st.sidebar.info("Built with Streamlit & Gemini / Grok")

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


# --- Execution ---
if research_btn and drug_input and api_key:
    summary = research_drug(drug_input, api_key, provider, selected_model)
    
    # Check for errors before saving to history
    is_error = any(phrase in summary for phrase in ["⚠️", "An error occurred", "No search results"])
    
    if not is_error:
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
