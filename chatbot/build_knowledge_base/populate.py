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
        print("Deleted the existing 'Formula-1' schema")

    # Create collection 'formula1'
    # TODO
    client.collections.create(
        name="formula1",
        properties=[
            wc.Property(name="circuitId", data_type=wc.DataType.NUMBER),
            wc.Property(name="circuitRef", data_type=wc.DataType.TEXT),
            wc.Property(name="name", data_type=wc.DataType.TEXT),
            wc.Property(name="location", data_type=wc.DataType.TEXT),
            wc.Property(name="country", data_type=wc.DataType.TEXT),
            # wc.Property(name="lat", data_type=wc.DataType.NUMBER), # JUISTE DATATYPE ???
            # wc.Property(name="lng", data_type=wc.DataType.NUMBER), # JUISTE DATATYPE ???
            # wc.Property(name="alt", data_type=wc.DataType.NUMBER),
            wc.Property(name="url", data_type=wc.DataType.TEXT),
        ],
        vectorizer_config=wc.Configure.Vectorizer.none(),
    )

    print("Created the 'Formula-1' schema")


def import_formula1_data(client):
    """" Import formula1 data to Weaviate """    
    
    if os.path.exists("/app/build_knowledge_base/datasets/circuits.csv"):
        df = pd.read_csv("/app/build_knowledge_base/datasets/circuits.csv")

        # TODO make my own embeddings
        embs_url = "/app/build_knowledge_base/datasets/embeddings/circuits.csv"
        emb_df = pd.read_csv(embs_url)
    

        formula1_data = client.collections.get("formula1")


        with formula1_data.batch.dynamic() as batch:
            for i, circuit in tqdm(enumerate(df.itertuples(index=False)), desc="Importing data to Weaviate"):
                # release_date = datetime.datetime.strptime(circuit.release_date, "%Y-%m-%d").replace(tzinfo=datetime.timezone.utc)
                print("circuit: ", circuit)
                print("")
                # genre_ids = json.loads(circuit.genre_ids)

                obj = {
                    "circuitId": circuit.circuitId,
                    "circuitRef": circuit.circuitRef,
                    "name": circuit.name,
                    "location": circuit.location,
                    "country": circuit.country,
                    # "lat": circuit.lat,
                    # "lng": circuit.lng,
                    # "alt": circuit.alt,
                    "url": circuit.url,
                }

                # Get the vector
                vector = emb_df.iloc[i].to_list()

                # add object, vector to batch queue
                batch.add_object(
                    properties=obj,
                    uuid=generate_uuid5(circuit.circuitId),
                    vector=vector
                )

        # Check if any objects failed to import
        if len(client.collections.get("formula1").batch.failed_objects) > 0:
            print(f"Failed to import {len(client.collections.get('formula1').batch.failed_objects)} objects")
    else:
        print("File not found: ./datasets/circuits.csv")



def get_collection_length(client):
    try:
        formula1_data = client.collections.get("formula1")
        return len(list(formula1_data.iterator()))
    except Exception as e:
        raise Exception(f"Could not get collection length: {str(e)}")
