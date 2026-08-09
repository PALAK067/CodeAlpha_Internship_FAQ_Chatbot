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

# Custom CSS to match the exact Gradio Rosegold Theme
st.markdown("""
<style>
/* Streamlit main container styling */
.stApp {
    background-image: url('https://upload.wikimedia.org/wikipedia/commons/thumb/e/e0/Code_Icon.svg/512px-Code_Icon.svg.png') !important;
    background-repeat: no-repeat !important;
    background-position: center center !important;
    background-attachment: fixed !important;
    background-size: 50% !important;
    background-color: #FDF4F5 !important;
}

/* Glassmorphism main card wrapper */
.block-container {
    background: rgba(255, 255, 255, 0.90) !important;
    backdrop-filter: blur(10px) !important;
    border-radius: 20px !important;
    box-shadow: 0 8px 32px 0 rgba(183, 110, 121, 0.2) !important;
    border: 1px solid rgba(183, 110, 121, 0.15) !important;
    padding: 2.5rem 3rem !important;
    margin-top: 2rem !important;
    max-width: 1200px !important;
}

/* Headings */
h1, h2, h3, h4 {
    color: #B76E79 !important;
    font-weight: 800 !important;
    text-shadow: 1px 1px 2px rgba(183, 110, 121, 0.1);
}

/* Suggested Questions Buttons */
div.stButton > button {
    background: rgba(183, 110, 121, 0.08) !important;
    border: 1px solid #B76E79 !important;
    color: #A25F69 !important;
    font-weight: 600 !important;
    margin-bottom: 8px !important;
    border-radius: 8px !important;
    transition: all 0.3s ease !important;
    text-align: left !important;
    width: 100% !important;
    padding: 0.6rem 1rem !important;
}
div.stButton > button:hover {
    background: #B76E79 !important;
    color: white !important;
    transform: translateY(-2px);
    box-shadow: 0 4px 12px rgba(183, 110, 121, 0.4) !important;
}

/* Send & Clear Primary Buttons */
.primary-btn button {
    background: linear-gradient(135deg, #B76E79 0%, #A25F69 100%) !important;
    border: none !important;
    color: white !important;
    font-weight: bold !important;
    box-shadow: 0 4px 15px rgba(183, 110, 121, 0.3) !important;
}
.primary-btn button:hover {
    transform: translateY(-2px);
    box-shadow: 0 6px 20px rgba(183, 110, 121, 0.5) !important;
}

/* Chat container panel */
.chat-panel {
    background-color: #FDF4F5;
    background-image: url('https://upload.wikimedia.org/wikipedia/commons/thumb/e/e0/Code_Icon.svg/512px-Code_Icon.svg.png');
    background-repeat: no-repeat;
    background-position: center center;
    background-size: 25%;
    border: 1px solid rgba(183, 110, 121, 0.25);
    border-radius: 12px;
    height: 480px;
    overflow-y: auto;
    padding: 1.2rem;
    display: flex;
    flex-direction: column;
    gap: 1rem;
}

/* User chat bubble */
.chat-bubble-user {
    align-self: flex-end;
    background: linear-gradient(135deg, #B76E79 0%, #A25F69 100%);
    color: white;
    padding: 10px 16px;
    border-radius: 12px 12px 0 12px;
    max-width: 80%;
    box-shadow: 0 3px 10px rgba(183, 110, 121, 0.25);
    font-size: 0.95rem;
    line-height: 1.4;
}

/* Bot chat bubble */
.chat-bubble-bot {
    align-self: flex-start;
    background-color: rgba(255, 255, 255, 0.95);
    border: 1px solid rgba(183, 110, 121, 0.3);
    border-left: 4px solid #B76E79;
    color: #4A3B3C;
    padding: 10px 16px;
    border-radius: 12px 12px 12px 0;
    max-width: 80%;
    box-shadow: 0 3px 10px rgba(183, 110, 121, 0.1);
    font-size: 0.95rem;
    line-height: 1.4;
}

/* Text Input container */
div[data-testid="stTextInput"] input {
    border: 1px solid rgba(183, 110, 121, 0.4) !important;
    border-radius: 8px !important;
    background-color: white !important;
    color: #333 !important;
}
div[data-testid="stTextInput"] input:focus {
    border-color: #B76E79 !important;
    box-shadow: 0 0 0 2px rgba(183, 110, 121, 0.2) !important;
}
</style>
""", unsafe_allow_html=True)

# App Header
st.markdown("""
<div style="text-align: center; margin-bottom: 1.5rem;">
    <h1 style="font-size: 2.8em; margin-bottom: 0;">✨ CodeAlpha Task 2: FAQ Chatbot</h1>
    <p style="font-size: 1.1em; color: #888; margin-top: 5px;">Your smart, rosegold-themed AI assistant for customer service.</p>
</div>
""", unsafe_allow_html=True)

# Initialize Session State
if "messages" not in st.session_state:
    st.session_state.messages = []

# Two-column layout matching Gradio exactly
col_left, col_right = st.columns([1, 2.3], gap="large")

# Left Column: Suggested Questions
with col_left:
    st.markdown("### 📌 Suggested Questions")
    st.markdown("<p style='font-size: 0.9em; color: #666;'>Click any question below to instantly ask the chatbot. These remain visible throughout your session.</p>", unsafe_allow_html=True)
    
    for q in questions:
        if st.button(q, key=f"btn_{q}"):
            st.session_state.messages.append({"role": "user", "content": q})
            resp = get_best_response(q)
            st.session_state.messages.append({"role": "bot", "content": resp})
            st.rerun()

# Right Column: Chat History and Input
with col_right:
    st.markdown("### 💬 Chat History")
    
    # Construct Chat HTML
    chat_content = ""
    if not st.session_state.messages:
        chat_content = "<div style='text-align: center; color: #999; margin: auto;'>👋 Welcome! Ask a question below or choose from the suggestions on the left.</div>"
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
