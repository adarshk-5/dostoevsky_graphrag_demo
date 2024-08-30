# Installing the Required Packages
## Install Ollama
First, download Ollama from https://ollama.com/download.  
Then, run the following commands in your terminal:
```
pip install ollama
ollama serve
ollama pull mistral
ollama pull nomic-embed-text
ollama pull llama3.1
```
## Install GraphRAG
```
pip install graphrag
```
## Install Streamlit
```
pip install streamlit
```

# Running the Demo with Ollama
## Modifying GraphRAG for Ollama
Change the following files to the versions in `/files_to_change` (the graphrag files will be found where your Python packages are saved)
- `graphrag/llm/openai/openai_embeddings_llm.py`
- `graphrag/query/llm/oai/embedding.py`  

## *(OPTIONAL)* Running the GraphRAG Pipeline 
You can proceed to the demo immediately, but if you want to run the pipeline yourself, run the following command in your terminal.  
*Note*: You may want to play with the settings in `settings.yaml` if you're running the pipeline yourself. Check the [GraphRAG documentation](https://microsoft.github.io/graphrag/posts/config/json_yaml/) for more details.
```
python3 -m graphrag.index --root ./dostoevsky_graphrag
```
Wait for the pipeline to finish running. Depending on your setup, this may take a while, so feel free to use the preloaded files instead.  
When the pipeline finishes, change the path for the variable *`data_dir`* in `graphrag_streamlit.py` to the folder with the completed parquet files (ex: `./dostoevsky_graphrag/output/<timestamp>/artifacts`)  

## Running the Demo
You can start the demo immediately with the preloaded files by running the following command in your terminal:
```
streamlit run graphrag_streamlit.py
```
This will open a window in your web browser where you can hold a conversation about Fyodor Dostoevsky's works. 