import requests
import pandas as pd
import requests
import os
from dotenv import load_dotenv

load_dotenv()

hf_token = os.getenv("HUGGINGFACE_APIKEY")

def query(texts):
    model_id = "sentence-transformers/all-MiniLM-L6-v2"

    api_url = f"https://api-inference.huggingface.co/pipeline/feature-extraction/{model_id}"
    headers = {"Authorization": f"Bearer {hf_token}"}

    response = requests.post(
        api_url,
        headers=headers,
        json={"inputs": texts, "options": {"wait_for_model": True}},
    )
    return response.json()


df = pd.read_csv("./datasets/movies_data_1990_2024.csv")

# Loop through the dataset to generate vectors in batches
emb_dfs = list()
src_texts = list()
for i, row in enumerate(df.itertuples(index=False)):
    # association between these embeddings and other properties of the movies is maintained through the indexing of the resulting DataFrame. 
    # so only the title and overview will be used for semantic similarity
    src_text = "Title" + row.title + "; Overview: " + row.overview 
    # Add to the buffer
    src_texts.append(src_text)
    if (len(src_texts) == 50) or (i + 1 == len(df)):  # Get embeddings in batches of 50
        # Get a batch of embeddings
        output = query(src_texts)
        emb_df = pd.DataFrame(output, index=src_texts)
        # Add the batch of embeddings to a list
        emb_dfs.append(emb_df)
        # Reset the buffer
        src_texts = list()


emb_df = pd.concat(emb_dfs)
emb_df.to_csv(
    f"./datasets/movies_data_1990_2024_embeddingsMY0WN.csv",
    index=False,
)