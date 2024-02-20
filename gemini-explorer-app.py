import vertexai
import streamlit as st
from vertexai.preview import generative_models
from vertexai.preview.generative_models import GenerativeModel, Part, Content

# Initiating your project name from GCP's project
project = "gemini-explorer-414913"
vertexai.init(project=project)

# Initiating your model's configuration
config = generative_models.GenerationConfig(
    temperature = 0.4,
    top_p = 0.59,
    top_k = 9,
    max_output_tokens = 2048
)

# Initiating your model selection with configuration earlier
model = GenerativeModel(
    "gemini-pro",
    generation_config = config
)

# Start the chat from model before
chat = model.start_chat()

# This is the function for answering from model
def model_answer(chat, query):
    
    # Take a response from a query for a spesific chat
    response = chat.send_message(query)

    # We take the output text from first candidate
    output = response.candidates[0].content.parts[0].text

    # The model write the output
    with st.chat_message("vertex-ai-model"):
        st.markdown(output)

    # Don't forget to update Session State messages
    # for the user and the model answered
    
    st.session_state.messages.append({
        "role": "user",
        "content": query
    })
    
    st.session_state.messages.append({
        "role": "vertex-ai-model",
        "content": output
    })

# This is only just for aesthetics of the Streamlit app
st.title("Gemini Explorer")

# Initiate empty array if Session State is empty
if "messages" not in st.session_state:
    st.session_state.messages = []

# Updating the chat history
for message in st.session_state.messages:
    
    content = Content(
        role = message["role"],
        parts = [Part.from_text(message["content"])]
    )
    
    chat.history.append(content)

# Add some initial prompt if message is empty
if len(st.session_state.messages) == 0:
    
    initial_prompt = "My name is Vertex, an assistant powered by Google Gemini."
    model_answer(chat, initial_prompt)

# Try to get the input from user
query = st.chat_input("What can Vertex do for you, friend?")

# If user inputted, write that input to the chat
if query:
    with st.chat_message("user"):
        st.markdown(query)

# Then model answer it to the chat
model_answer(chat, query)