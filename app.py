import json
import gradio as gr
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

# Load FAQs from JSON file
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
processed_questions = [preprocess(q) for q in questions]

# Initialize TF-IDF Vectorizer and fit it to our processed questions
vectorizer = TfidfVectorizer()
if processed_questions:
    question_vectors = vectorizer.fit_transform(processed_questions)

def get_best_response(user_query, history):
    if not processed_questions:
        history.append({"role": "user", "content": user_query})
        history.append({"role": "assistant", "content": "FAQ database is empty."})
        return "", history
        
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

    # Append to history in Gradio 6.0+ format
    history.append({"role": "user", "content": user_query})
    history.append({"role": "assistant", "content": response})
    
    return "", history

def load_example(example_text, history):
    return get_best_response(example_text, history)

# Custom Rosegold & Pastel Theme CSS
custom_css = """
/* Body background with watermark - Light Pastel */
body {
    background-image: url('https://upload.wikimedia.org/wikipedia/commons/thumb/e/e0/Code_Icon.svg/512px-Code_Icon.svg.png') !important;
    background-repeat: no-repeat !important;
    background-position: center center !important;
    background-attachment: fixed !important;
    background-size: 50% !important;
    background-color: #FDF4F5 !important; /* Light Pastel Pink/Rose */
}

/* Semi-transparent overlay to ensure watermark is visible but not overpowering */
.gradio-container {
    background: rgba(255, 255, 255, 0.85) !important;
    backdrop-filter: blur(10px) !important;
    border-radius: 20px !important;
    box-shadow: 0 8px 32px 0 rgba(183, 110, 121, 0.2) !important;
    border: 1px solid rgba(183, 110, 121, 0.15) !important;
}

/* Dark mode overrides for watermark and overlay */
.dark body {
    background-color: #2D1E20 !important; /* Deep Rosewood for dark mode */
}
.dark .gradio-container {
    background: rgba(45, 30, 32, 0.85) !important;
    box-shadow: 0 8px 32px 0 rgba(183, 110, 121, 0.15) !important;
    border: 1px solid rgba(183, 110, 121, 0.3) !important;
}

/* Rosegold Accent Colors for Texts and Buttons */
h1, h2, h3 {
    color: #B76E79 !important; /* Rosegold */
    font-weight: 800 !important;
    text-shadow: 1px 1px 2px rgba(183, 110, 121, 0.1);
}

.dark h1, .dark h2, .dark h3 {
    color: #E0A6AF !important; /* Lighter Rosegold for dark mode */
}

/* Button styling */
button.primary {
    background: linear-gradient(135deg, #B76E79 0%, #A25F69 100%) !important;
    border: none !important;
    color: white !important;
    font-weight: bold !important;
    box-shadow: 0 4px 15px rgba(183, 110, 121, 0.3) !important;
}
button.primary:hover {
    transform: translateY(-2px);
    box-shadow: 0 6px 20px rgba(183, 110, 121, 0.5) !important;
}

/* Sidebar suggestion buttons */
.suggestion-btn {
    background: rgba(183, 110, 121, 0.08) !important;
    border: 1px solid #B76E79 !important;
    color: #A25F69 !important;
    margin-bottom: 8px !important;
    border-radius: 8px !important;
    transition: all 0.3s ease !important;
    text-align: left !important;
}
.dark .suggestion-btn {
    color: #E0A6AF !important;
    background: rgba(183, 110, 121, 0.15) !important;
}
.suggestion-btn:hover {
    background: #B76E79 !important;
    color: white !important;
}

/* Chatbot overall container (panel) */
.panel {
    background-color: #FDF4F5 !important;
    background-image: url('https://upload.wikimedia.org/wikipedia/commons/thumb/e/e0/Code_Icon.svg/512px-Code_Icon.svg.png') !important;
    background-repeat: no-repeat !important;
    background-position: center center !important;
    background-size: 30% !important;
    border: 1px solid rgba(183, 110, 121, 0.2) !important;
}
.dark .panel {
    background-color: #2D1E20 !important;
    border: 1px solid rgba(183, 110, 121, 0.4) !important;
}

/* User chat bubble */
.user {
    background: linear-gradient(135deg, #B76E79 0%, #A25F69 100%) !important;
    border-radius: 12px 12px 0 12px !important;
}
.user * {
    color: white !important;
}

/* Chat bubble styling */
.bot {
    background-color: rgba(183, 110, 121, 0.15) !important;
    border: 1px solid rgba(183, 110, 121, 0.3) !important;
    border-left: 4px solid #B76E79 !important;
    border-radius: 12px 12px 12px 0 !important;
}
.bot * {
    color: #4A3B3C !important;
}
.dark .bot {
    background-color: rgba(183, 110, 121, 0.25) !important;
}
.dark .bot * {
    color: #FDF4F5 !important;
}
"""

with gr.Blocks() as demo:
    gr.HTML(
        '''
        <div style="text-align: center; margin-bottom: 1rem;">
            <h1 style="font-size: 3em; margin-bottom: 0;">✨ CodeAlpha Task 2: FAQ Chatbot</h1>
            <p style="font-size: 1.1em; color: gray;">Your smart, rosegold-themed AI assistant for customer service.</p>
        </div>
        '''
    )
    
    with gr.Row():
        # Sidebar for persistent FAQs
        with gr.Column(scale=1, min_width=300):
            gr.Markdown("### 📌 Suggested Questions")
            gr.Markdown("Click any question below to instantly ask the chatbot. These remain visible throughout your session.")
            
            # Create a button for each FAQ question
            suggestion_btns = []
            for q in questions:
                btn = gr.Button(q, elem_classes="suggestion-btn")
                suggestion_btns.append(btn)
                
            gr.Markdown("### ⚙️ Theme")
            theme_btn = gr.Button("🌓 Toggle Day/Night Theme")                
        # Main Chat Area
        with gr.Column(scale=3):
            chatbot = gr.Chatbot(
                label="Chat History", 
                height=500
            )
            
            with gr.Row():
                msg = gr.Textbox(
                    show_label=False,
                    placeholder="Type your question here and press Enter...",
                    container=False,
                    scale=8
                )
                submit_btn = gr.Button("Send", variant="primary", scale=1)
                clear_btn = gr.ClearButton([msg, chatbot], value="Clear History", scale=1)

    # Event handlers
    msg.submit(get_best_response, [msg, chatbot], [msg, chatbot])
    submit_btn.click(get_best_response, [msg, chatbot], [msg, chatbot])
    
    # Attach click events to suggestion buttons
    for btn in suggestion_btns:
        btn.click(load_example, inputs=[btn, chatbot], outputs=[msg, chatbot])
        
    # Manual theme toggle logic
    theme_btn.click(None, None, None, js="""
    function() {
        document.body.classList.toggle('dark');
    }
    """)

if __name__ == "__main__":
    demo.launch(server_name="0.0.0.0", server_port=7861, css=custom_css)
