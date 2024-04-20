import os
import json
import requests
import pandas as pd
import datetime
from dotenv import load_dotenv
from tqdm import tqdm
from weaviate.util import generate_uuid5
import weaviate.classes.config as wc

load_dotenv()



def create_formula1_collection(client):
    # check if the schema already exists
    if client.collections.exists("formula1"):
        client.collections.delete("formula1")
        print("Deleted the existing 'Movies' schema")

    # Create collection 'Movies'
    client.collections.create(
        name="formula1",
        properties=[
            wc.Property(name="position", data_type=wc.DataType.NUMBER),
            wc.Property(name="points", data_type=wc.DataType.NUMBER),
            wc.Property(name="laps", data_type=wc.DataType.NUMBER),
            wc.Property(name="rank", data_type=wc.DataType.NUMBER),
            wc.Property(name="year", data_type=wc.DataType.NUMBER),
            wc.Property(name="name_x", data_type=wc.DataType.TEXT),
            wc.Property(name="name_y", data_type=wc.DataType.TEXT),
            wc.Property(name="location", data_type=wc.DataType.TEXT),
            wc.Property(name="country", data_type=wc.DataType.TEXT),
            wc.Property(name="forename", data_type=wc.DataType.TEXT),
            wc.Property(name="surname", data_type=wc.DataType.TEXT),
            wc.Property(name="nationality_x", data_type=wc.DataType.TEXT),
            wc.Property(name="name", data_type=wc.DataType.TEXT),
            wc.Property(name="status", data_type=wc.DataType.TEXT),
        ],
        vectorizer_config=wc.Configure.Vectorizer.none(),
    )



def import_formula1_data(client):
    """" Import movies data to Weaviate """    
    
    if os.path.exists("/app/build_knowledge_base/merged_data.csv"):
        df = pd.read_csv("/app/build_knowledge_base/merged_data.csv")
        df = df.head(100)

        embs_url = "/app/build_knowledge_base/datasets/embeddings/merged_data.csv"
        emb_df = pd.read_csv(embs_url)
        emb_df = emb_df.head(100)

        formula1_data = client.collections.get("formula1")

        with formula1_data.batch.dynamic() as batch:
            for i, row in tqdm(enumerate(df.itertuples(index=False)), desc="Importing Movies"):
         

                movie_obj = {
                    "position": int(row.position),
                    "points": int(row.points),
                    "laps": int(row.laps),
                    "rank": int(row.rank),
                    "year": int(row.year),
                    "name_x": row.name_x,
                    "name_y": row.name_y,
                    "location": row.location,
                    "country": row.country,
                    "forename": row.forename,
                    "surname": row.surname,
                    "nationality_x": row.nationality_x,
                    "name": row.name,
                    
                    

                    "status": row.status,
                
                }

                # Get the vector
                vector = emb_df.iloc[i].to_list()

                # add object, vector to batch queue
                batch.add_object(
                    properties=movie_obj,
                    uuid=generate_uuid5(str(i)),
                    vector=vector
                )

        # Check if any objects failed to import
        if len(client.collections.get("formula1").batch.failed_objects) > 0:
            print(f"Failed to import {len(client.collections.get('formula1').batch.failed_objects)} objects")
    else:
        print("File not found: ./datasets/movies_data_1990_2024.csv")



def get_collection_length(client):
    try:
        movies = client.collections.get("formula1")
        return len(list(movies.iterator()))
    except Exception as e:
        raise Exception(f"Could not get collection length: {str(e)}")
