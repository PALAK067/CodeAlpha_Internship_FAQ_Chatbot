import json
import streamlit as st
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import string
import os

# Download necessary NLTK datasets
try:
    nltk.data.find('tokenizers/punkt')
    nltk.data.find('tokenizers/punkt_tab')
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('punkt', quiet=True)
    nltk.download('punkt_tab', quiet=True)
    nltk.download('stopwords', quiet=True)

# Page configuration
st.set_page_config(page_title="CodeAlpha Task 2: FAQ Chatbot", page_icon="✨", layout="wide")

# Initialize Session State
if "messages" not in st.session_state:
    st.session_state.messages = []
if "theme" not in st.session_state:
    st.session_state.theme = "light"

# Load FAQs from JSON file
@st.cache_data
def load_faqs(filepath='faqs.json'):
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            faqs = json.load(f)
        return faqs
    except FileNotFoundError:
        return []

faqs = load_faqs()
questions = [faq['question'] for faq in faqs]
answers = [faq['answer'] for faq in faqs]

# Preprocessing setup
stop_words = set(stopwords.words('english'))

def preprocess(text):
    """Tokenize, lower case, remove stopwords and punctuation."""
    tokens = word_tokenize(text.lower())
    tokens = [t for t in tokens if t not in stop_words and t not in string.punctuation]
    return " ".join(tokens)

# Preprocess all stored FAQ questions
@st.cache_resource
def get_nlp_model(all_questions):
    processed_questions = [preprocess(q) for q in all_questions]
    vectorizer = TfidfVectorizer()
    question_vectors = None
    if processed_questions:
        question_vectors = vectorizer.fit_transform(processed_questions)
    return vectorizer, question_vectors, processed_questions

vectorizer, question_vectors, processed_questions = get_nlp_model(questions)

def get_best_response(user_query):
    if not processed_questions:
        return "FAQ database is empty."
        
    # Preprocess user query
    processed_query = preprocess(user_query)
    
    # Vectorize user query
    user_vector = vectorizer.transform([processed_query])
    
    # Calculate cosine similarity between the query and all FAQ questions
    similarities = cosine_similarity(user_vector, question_vectors)
    
    # Find the most similar question index
    best_match_idx = similarities.argmax()
    best_score = similarities[0][best_match_idx]
    
    # Similarity threshold to avoid matching completely irrelevant questions
    THRESHOLD = 0.2
    
    if best_score > THRESHOLD:
        response = answers[best_match_idx]
    else:
        response = "I'm sorry, I couldn't find an exact answer to your question in my FAQ database. Could you try rephrasing it, or select one of the suggested options from the sidebar? 🤔"

    return response

# Dynamic Theme Colors
is_dark = st.session_state.theme == "dark"

bg_app = "#1E1214" if is_dark else "#FDF4F5"
bg_container = "rgba(38, 24, 27, 0.94)" if is_dark else "rgba(255, 255, 255, 0.90)"
border_container = "rgba(224, 166, 175, 0.3)" if is_dark else "rgba(183, 110, 121, 0.15)"
text_heading = "#E0A6AF" if is_dark else "#B76E79"
text_subtitle = "#D4B0B7" if is_dark else "#888888"
btn_bg = "rgba(224, 166, 175, 0.12)" if is_dark else "rgba(183, 110, 121, 0.08)"
btn_border = "#E0A6AF" if is_dark else "#B76E79"
btn_color = "#E0A6AF" if is_dark else "#A25F69"
chat_bg = "#25171A" if is_dark else "#FDF4F5"
chat_border = "rgba(224, 166, 175, 0.3)" if is_dark else "rgba(183, 110, 121, 0.25)"
bot_bubble_bg = "rgba(45, 30, 34, 0.95)" if is_dark else "rgba(255, 255, 255, 0.95)"
bot_bubble_text = "#FDF4F5" if is_dark else "#4A3B3C"
bot_bubble_border = "#E0A6AF" if is_dark else "#B76E79"
input_bg = "#2D1E20" if is_dark else "#FFFFFF"
input_text = "#FDF4F5" if is_dark else "#333333"
input_border = "rgba(224, 166, 175, 0.4)" if is_dark else "rgba(183, 110, 121, 0.4)"

# Custom CSS
st.markdown(f"""
<style>
/* Main App Background with Watermark */
.stApp {{
    background-image: url('https://upload.wikimedia.org/wikipedia/commons/thumb/e/e0/Code_Icon.svg/512px-Code_Icon.svg.png') !important;
    background-repeat: no-repeat !important;
    background-position: center center !important;
    background-attachment: fixed !important;
    background-size: 50% !important;
    background-color: {bg_app} !important;
    color: {bot_bubble_text} !important;
}}

/* Glassmorphism Main Card Container */
.block-container {{
    background: {bg_container} !important;
    backdrop-filter: blur(12px) !important;
    border-radius: 20px !important;
    box-shadow: 0 8px 32px 0 rgba(0, 0, 0, {'0.5' if is_dark else '0.15'}) !important;
    border: 1px solid {border_container} !important;
    padding: 2.5rem 3rem !important;
    margin-top: 2rem !important;
    max-width: 1200px !important;
}}

/* Headings */
h1, h2, h3, h4 {{
    color: {text_heading} !important;
    font-weight: 800 !important;
    text-shadow: 1px 1px 2px rgba(183, 110, 121, 0.1);
}}

/* Suggested Question Buttons */
div.stButton > button {{
    background: {btn_bg} !important;
    border: 1px solid {btn_border} !important;
    color: {btn_color} !important;
    font-weight: 600 !important;
    margin-bottom: 8px !important;
    border-radius: 8px !important;
    transition: all 0.3s ease !important;
    text-align: left !important;
    width: 100% !important;
    padding: 0.6rem 1rem !important;
}}
div.stButton > button:hover {{
    background: {btn_border} !important;
    color: {'#1E1214' if is_dark else 'white'} !important;
    transform: translateY(-2px);
    box-shadow: 0 4px 12px rgba(183, 110, 121, 0.4) !important;
}}

/* Primary Action Buttons */
.primary-btn button {{
    background: linear-gradient(135deg, #B76E79 0%, #A25F69 100%) !important;
    border: none !important;
    color: white !important;
    font-weight: bold !important;
    box-shadow: 0 4px 15px rgba(183, 110, 121, 0.3) !important;
}}
.primary-btn button:hover {{
    transform: translateY(-2px);
    box-shadow: 0 6px 20px rgba(183, 110, 121, 0.5) !important;
    color: white !important;
}}

/* Chat Container Panel */
.chat-panel {{
    background-color: {chat_bg};
    background-image: url('https://upload.wikimedia.org/wikipedia/commons/thumb/e/e0/Code_Icon.svg/512px-Code_Icon.svg.png');
    background-repeat: no-repeat;
    background-position: center center;
    background-size: 25%;
    border: 1px solid {chat_border};
    border-radius: 12px;
    height: 480px;
    overflow-y: auto;
    padding: 1.2rem;
    display: flex;
    flex-direction: column;
    gap: 1rem;
}}

/* User Chat Bubble */
.chat-bubble-user {{
    align-self: flex-end;
    background: linear-gradient(135deg, #B76E79 0%, #A25F69 100%);
    color: white;
    padding: 10px 16px;
    border-radius: 12px 12px 0 12px;
    max-width: 80%;
    box-shadow: 0 3px 10px rgba(183, 110, 121, 0.25);
    font-size: 0.95rem;
    line-height: 1.4;
}}

/* Bot Chat Bubble */
.chat-bubble-bot {{
    align-self: flex-start;
    background-color: {bot_bubble_bg};
    border: 1px solid {chat_border};
    border-left: 4px solid {bot_bubble_border};
    color: {bot_bubble_text};
    padding: 10px 16px;
    border-radius: 12px 12px 12px 0;
    max-width: 80%;
    box-shadow: 0 3px 10px rgba(0, 0, 0, 0.1);
    font-size: 0.95rem;
    line-height: 1.4;
}}

/* Text Input Styling */
div[data-testid="stTextInput"] input {{
    border: 1px solid {input_border} !important;
    border-radius: 8px !important;
    background-color: {input_bg} !important;
    color: {input_text} !important;
}}
div[data-testid="stTextInput"] input:focus {{
    border-color: {text_heading} !important;
    box-shadow: 0 0 0 2px rgba(183, 110, 121, 0.2) !important;
}}
</style>
""", unsafe_allow_html=True)

# App Header
st.markdown(f"""
<div style="text-align: center; margin-bottom: 1.5rem;">
    <h1 style="font-size: 2.8em; margin-bottom: 0;">✨ CodeAlpha Task 2: FAQ Chatbot</h1>
    <p style="font-size: 1.1em; color: {text_subtitle}; margin-top: 5px;">Your smart, rosegold-themed AI assistant for customer service.</p>
</div>
""", unsafe_allow_html=True)

# Two-column layout matching Gradio exactly
col_left, col_right = st.columns([1, 2.3], gap="large")

# Left Column: Suggested Questions & Theme Settings
with col_left:
    st.markdown("### 📌 Suggested Questions")
    st.markdown(f"<p style='font-size: 0.9em; color: {text_subtitle};'>Click any question below to instantly ask the chatbot. These remain visible throughout your session.</p>", unsafe_allow_html=True)
    
    for q in questions:
        if st.button(q, key=f"btn_{q}"):
            st.session_state.messages.append({"role": "user", "content": q})
            resp = get_best_response(q)
            st.session_state.messages.append({"role": "bot", "content": resp})
            st.rerun()
            
    st.markdown("---")
    st.markdown("### ⚙️ Theme Settings")
    theme_label = "☀️ Switch to Light Pastel Theme" if is_dark else "🌙 Switch to Deep Rosewood Dark Theme"
    if st.button(theme_label, key="toggle_theme_btn"):
        st.session_state.theme = "light" if is_dark else "dark"
        st.rerun()

# Right Column: Chat History and Input
with col_right:
    st.markdown("### 💬 Chat History")
    
    # Construct Chat HTML
    chat_content = ""
    if not st.session_state.messages:
        chat_content = f"<div style='text-align: center; color: {text_subtitle}; margin: auto;'>👋 Welcome! Ask a question below or choose from the suggestions on the left.</div>"
    else:
        for msg in st.session_state.messages:
            if msg["role"] == "user":
                chat_content += f"<div class='chat-bubble-user'>{msg['content']}</div>"
            else:
                chat_content += f"<div class='chat-bubble-bot'>{msg['content']}</div>"
                
    st.markdown(f"<div class='chat-panel'>{chat_content}</div>", unsafe_allow_html=True)
    st.write("") # spacing
    
    # Form for User Input
    with st.form(key="chat_form", clear_on_submit=True):
        input_col, send_col = st.columns([4, 1])
        with input_col:
            user_input = st.text_input("Message", placeholder="Type your question here and press Enter...", label_visibility="collapsed")
        with send_col:
            st.markdown('<div class="primary-btn">', unsafe_allow_html=True)
            submit = st.form_submit_button("Send 🚀", use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)
            
    if submit and user_input.strip():
        st.session_state.messages.append({"role": "user", "content": user_input.strip()})
        resp = get_best_response(user_input.strip())
        st.session_state.messages.append({"role": "bot", "content": resp})
        st.rerun()
        
    if st.button("🗑️ Clear History", key="clear_history_btn"):
        st.session_state.messages = []
        st.rerun()
