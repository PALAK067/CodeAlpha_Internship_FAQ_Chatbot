# Task 2: FAQ Chatbot

This project is part of the CodeAlpha Artificial Intelligence Internship. It is a simple AI-powered chatbot that automatically answers Frequently Asked Questions (FAQs).

It uses Natural Language Processing (NLP) techniques to match user questions with predefined FAQs. 

## How It Works
1. Predefined FAQs are loaded from `faqs.json`.
2. Both the dataset questions and the user's input are preprocessed using `nltk` (tokenization, stopword removal).
3. The questions are transformed into numerical vectors using `TfidfVectorizer` from `scikit-learn`.
4. We calculate the **Cosine Similarity** between the user's vectorized input and the dataset's questions.
5. The chatbot returns the answer to the most similar question, provided the similarity exceeds a set threshold.

## Installation

1. Ensure you have Python installed.
2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```
   *(Note: The `app.py` script will automatically download the necessary NLTK datasets like 'punkt' and 'stopwords' on its first run.)*

## Usage

1. Run the application:
   ```bash
   python app.py
   ```
2. Open your web browser and navigate to the local URL provided by Gradio (typically `http://127.0.0.1:7861`).
3. Type a question in the chat interface (e.g., "What is your return policy?") and see the AI's response.
4. You can edit the `faqs.json` file to add your own custom questions and answers!
