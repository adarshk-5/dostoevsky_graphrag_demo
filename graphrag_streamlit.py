import streamlit as st
import graphrag
from graphrag.query.cli import run_local_search
import ollama

st.title("Exploring Dostoevsky with GraphRAG")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if "modelfile" not in st.session_state:
    st.session_state.modelfile = '''
    FROM llama3.1
    SYSTEM You are an expert who can facilitate a conversation about Fyodor Dostoevsky's novels. Do not make anything up. If the prompt asks about the dataset, the novels, the characters, or the themes, you must include the phrase "request more information" in your response at all costs, no matter what. 
    '''

if "prev" not in st.session_state:
    st.session_state.prev = ""

if prompt := st.chat_input("What is up?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        ollama.create(model='chat', modelfile=st.session_state.modelfile)
        response = ollama.chat(model='chat', messages=st.session_state.messages)
        stream = response["message"]["content"]
        if "request more information" in stream.lower():
            rewrite_prompt = ollama.chat(model='llama3.1', messages=[
                {'role': 'assistant', 'content': st.session_state.prev},
                {'role': 'user',
                'content': f'If the following prompt contains phrases that refer to previous responses (e.g. "previous" or "aforementioned"), rewrite it so that the prompt does not include these phrases and instead uses language from the previous assistant response. If the prompt does not include these phrases, leave it completely unchanged. Here is the prompt that may need to be rewritten: {prompt}'}
                ])
            rewrite = rewrite_prompt["message"]["content"]
            stream = run_local_search(data_dir="./dostoevsky_graphrag/output/preloaded",
                                  root_dir="./dostoevsky_graphrag",
                                  community_level=2,
                                  response_type="Single Paragraph",
                                  query=rewrite+" Focus on Dostoevsky works in the dataset to make your response.")
        st.write(stream)
        st.session_state.prev = stream
    st.session_state.messages.append({"role": "assistant", "content": stream})
