import streamlit as st
import replicate
import os
from langchain_community.text_embeddings import HuggingFaceEmbeddings
import utilities as utilities
from chromadb import Documents, EmbeddingFunction, Embeddings
import chromadb
from chromadb.config import Settings

# Set assistant icon to Snowflake logo
icons = {"assistant": "⛷️", "user": "⛷️"}

# App title
st.set_page_config(page_title="Contract Highlights")
replicate = replicate.Client(api_token='r8_S2BjENRSxC1IKR7Bt9WzqKylBmclcph3FIEQ8')

# Replicate Credentials
with st.sidebar:
    st.title('Snowflake Arctic')
    st.subheader("Select file")
    files_list = utilities.get_files_list()
    def on_change_file():
        response = generate_arctic_response()
        st.write_stream(response)
    file = st.selectbox("Please select contract",files_list,key="file",on_change=on_change_file)
    

def create_chroma_db(documents, path, name):
    """
    Creates a Chroma database using the provided documents, path, and collection name.

    Parameters:
    - documents: An iterable of documents to be added to the Chroma database.
    - path (str): The path where the Chroma database will be stored.
    - name (str): The name of the collection within the Chroma database.

    Returns:
    - Tuple[chromadb.Collection, str]: A tuple containing the created Chroma Collection and its name.
    """
    chroma_client = chromadb.PersistentClient(path=path,settings=Settings(allow_reset=True))
    db = chroma_client.get_or_create_collection(name=name)
    chroma_client.delete_collection(name=name)
    db = chroma_client.create_collection(name=name, embedding_function=GeminiEmbeddingFunction())

    for i, d in enumerate(documents):
        db.add(documents=d, ids=str(i))

    return db, name


# Function for generating Snowflake Arctic response
def generate_arctic_response():
    text = utilities.load_pdf('Files/Authorized Google Reseller Agreement.pdf')
    prompt_txt = f"""Provide all dates along with event details from given text in form of json array with keys like Timestamp, EventType, EventDescription
     in descending order of Timestamp: {text.replace("  ","")}"""
    prompt = []
    prompt.append("<|im_start|>user\n" + prompt_txt + "<|im_end|>")
    prompt.append("<|im_start|>assistant")
    prompt.append("")
    prompt_str = "\n".join(prompt)
    
    for event in replicate.stream("snowflake/snowflake-arctic-instruct",
                           input={"prompt": prompt_str,
                                  "prompt_template": r"{prompt}"
                                  }):
        yield str(event)


