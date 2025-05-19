import gradio as gr
import requests

API_URL_CONTEXT = "https://search-qna-production.up.railway.app/context"
API_URL_ANSWER = "https://search-qna-production.up.railway.app/answer"

latest_context_id = None

def submit_context(context_text):
    global latest_context_id
    response = requests.post(API_URL_CONTEXT, json={"context_text": context_text})
    latest_context_id = response.json().get("context_id")
    if not latest_context_id:
        return "Context storing failed"
    return "Context stored successfully!"

def ask_question(question):
    if not latest_context_id:
        return "Please submit a context first!"
    
    response = requests.post(API_URL_ANSWER, json={"context_id": latest_context_id, "question": question})
    return response.json().get("answer", "No answer found")

# Define UI elements
context_ui = gr.Interface(
    fn=submit_context,
    inputs=["text"],
    outputs="text",
    title="Submit Context"
)

question_ui = gr.Interface(
    fn=ask_question,
    inputs=["text"],
    outputs="text",
    title="Ask a Question"
)

# Launch UI with automatic context handling
ui = gr.TabbedInterface([context_ui, question_ui], ["Submit Context", "Ask Question"])
ui.launch()
