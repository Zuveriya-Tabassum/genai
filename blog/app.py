import streamlit as st
import os
import google.generativeai as genai

# Set API Key securely (Use environment variables in production)
os.environ['GEMINI_API_KEY'] = 'AIzaSyDhNBPxFPvwArIBlNc1hk0s8JKYmo6-yek'  # Replace with a secure method in production

genai.configure(api_key=os.environ['GEMINI_API_KEY'])

# Load the Gemini model
model = genai.GenerativeModel("gemini-1.5-flash")
chat = model.start_chat()

# Function to get AI response
def get_gemini_response(question):
    response = chat.send_message(question, stream=True)
    return "".join([chunk.text for chunk in response])

# Set page configuration (Wide layout)
st.set_page_config(page_title="Infobot", layout="wide")

# Initialize theme state (Default: Dark Mode)
if "dark_mode" not in st.session_state:
    st.session_state.dark_mode = True  

# Define background gradients
if st.session_state.dark_mode:
    gradient_bg = "linear-gradient(135deg, #141E30, #243B55)"  # Dark Mode
    text_color = "#FFFFFF"
else:
    gradient_bg = "linear-gradient(135deg, #FF9A8B, #FF6A88, #FF99AC)"  # Light Mode
    text_color = "#000000"

# Apply styles dynamically
st.markdown(f"""
    <style>
        html, body, [data-testid="stAppViewContainer"], [data-testid="stHeader"], 
        [data-testid="stToolbar"], [data-testid="stSidebar"], [data-testid="stFooter"] {{
            background: {gradient_bg} !important;
            background-attachment: fixed;
            background-size: cover;
            color: {text_color};
        }}

        .stTextInput>div>div>input {{
            border-radius: 10px;
            padding: 12px;
            border: 2px solid white;
            background-color: rgba(255, 255, 255, 0.2);
            color: {text_color};
        }}

        .stButton>button {{
            background: rgba(255, 255, 255, 0.2);
            border: none;
            border-radius: 50px;
            padding: 10px 15px;
            color: white;
            font-size: 18px;
            transition: 0.3s;
        }}
        .stButton>button:hover {{
            background: rgba(255, 255, 255, 0.4);
        }}

        .stChatMessage {{
            background-color: rgba(255, 255, 255, 0.1);
            padding: 10px;
            border-radius: 10px;
        }}

        /* Style to position title beside toggle, increase font size and add space */
        .stApp > header {{
            # display: flex;
            align-items: center;
            justify-content: space-between; /* Distribute space between items */
            padding: 20px 30px;  /* Add padding */
        }}

        .stApp > header > h1 {{
            font-size: 5em; /* Increase title font size */
            margin: 0; /* Remove default margin */
        }}

    </style>
""", unsafe_allow_html=True)

# Header - placed here to ensure styling applies
col1, col2 = st.columns([0.9, 0.1])  # 90% for the content, 10% for the toggle

with col1:
    st.header("Infobot AI Chat")

with col2:
    st.session_state.dark_mode = st.toggle("", value=st.session_state.dark_mode, key="theme_toggle")  # Use key to differentiate

# Initialize chat history
if "chat_history" not in st.session_state:
    st.session_state["chat_history"] = []

# **All Sections Side by Side**
col1, col2, col3 = st.columns([1, 1, 1])

# New Chat Button
with col1:
    if st.button("New Chat", use_container_width=True):
        st.session_state["chat_history"] = []
        st.rerun()

# Chat History
with col2:
    show_history = st.button("Chat History", use_container_width=True)

# Expand Chat History if Requested
with col2:
    if show_history:
        with st.expander("📖 Chat History", expanded=True):
            for role, text in st.session_state["chat_history"]:
                with st.chat_message("user" if role == "You" else "assistant"):
                    st.write(text)

# Chat input (Placed at the bottom)
user_input = st.chat_input("Ask a question...")

if user_input:
    with st.chat_message("user"):
        st.write(user_input)

    st.session_state["chat_history"].append(("You", user_input))

    # Show a loading spinner while AI is responding
    with st.spinner("🤖 Thinking..."):
        response_text = get_gemini_response(user_input)

    with st.chat_message("assistant"):
        st.write(response_text)

    st.session_state["chat_history"].append(("Bot", response_text))
