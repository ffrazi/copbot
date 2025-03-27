import streamlit as st
import requests
import webbrowser
import base64

# Backend URL
BACKEND_URL = "http://127.0.0.1:5001/api/chatbot"
GOOGLE_MAPS_SEARCH_URL = "https://www.google.com/maps/search/?api=1&query=police+station+near+me"

# Load and encode the logo image as base64
def get_base64_of_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode()

# Path to the Tamil Nadu Police logo
logo_path = r"C:\Users\fazfa\OneDrive\Desktop\copbot\CopBotChatbox\backend\static\logo.jpg"
logo_base64 = get_base64_of_image(logo_path)
background_image = f"data:image/jpg;base64,{logo_base64}"

# Custom CSS for background image
st.markdown(f"""
    <style>
    .stApp {{
        background-color:transparent;
    }}
    .background-container {{
        position: fixed;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%);
        width: 70%;
        height: 100%;
        background-image: url("{background_image}");
        background-size: 70% 100%;
        background-position: center;
        background-repeat: no-repeat;
        opacity: 0.2;
        z-index: -1;
    }}
    .stTitle {{
        color: #2c3e50;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
    }}
    .stTextInput > div > div > input {{
        background-color: rgba(255, 255, 255, 0.8);
        color: #2c3e50;
        border: 1px solid #bdc3c7;
    }}
    .stButton > button {{
        background-color: #34495e !important;
        color: white !important;
        border: none;
    }}
    .stFileUploader > div > div > div {{
        background-color: #2c3e50;
        color: white;
        border: none;
    }}
    .stFileUploader > div > div > div > div > p {{
        color: #bdc3c7;
    }}
    </style>
    <div class="background-container"></div>
    """, unsafe_allow_html=True)

st.title("CopBot Chatbox 🕵‍♂")

# User input
user_input = st.text_input("Ask CopBot:", "")

col1, col2 = st.columns([3, 1])
with col1:
    send_button = st.button("Send")
with col2:
    sos_button = st.button("🚨 - Find Nearest Police Station")

if send_button:
    if user_input.strip():
        # Prepare payload
        payload = {"message": user_input}
        
        # Add file to payload if uploaded
        if 'uploaded_file' in st.session_state and st.session_state.uploaded_file is not None:
            files = {
                'file': (st.session_state.uploaded_file.name, st.session_state.uploaded_file, st.session_state.uploaded_file.type)
            }
            response = requests.post(BACKEND_URL, data={"message": user_input}, files=files)
        else:
            response = requests.post(BACKEND_URL, json={"message": user_input})
        
        if response.status_code == 200:
            bot_reply = response.json().get("response", "No response from bot.")
            st.write(f"*CopBot:* {bot_reply}")
        else:
            st.error("Error connecting to backend!")

if sos_button:
    webbrowser.open(GOOGLE_MAPS_SEARCH_URL)

# Separate section for file upload at the bottom
st.markdown("---")
st.subheader("Optional File Upload")

# File upload section moved to the bottom
uploaded_file = st.file_uploader("Upload a supporting document:", type=['pdf', 'txt', 'docx', 'jpg', 'png'])

# Store uploaded file in session state
if uploaded_file is not None:
    st.session_state.uploaded_file = uploaded_file
    st.write(f"Uploaded file: {uploaded_file.name}")
else:
    # Remove uploaded file from session state if no file is present
    if 'uploaded_file' in st.session_state:
        del st.session_state.uploaded_file