""" This retriever class gets data from weaviate and returns it to the user. """

import os
import requests
import weaviate
import weaviate.classes.query as wq
import weaviate.classes.config as wc
import pandas as pd
from typing import List, Union
from weaviate.classes.query import MetadataQuery
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer
from dotenv import load_dotenv
load_dotenv()

hf_token = os.getenv("HUGGINGFACE_APIKEY")

from prompts import (
    INSTRUCTION_PROMPT
)



class Retriever():
    def __init__(self): 
        self.client = self.connect_to_weaviate()

    def connect_to_weaviate(self):
        try:
            return weaviate.connect_to_local(host="weaviate", port=8080)
        except Exception as e:
            raise Exception(f"Could not connect to Weaviate: {str(e)}")
        
    def query_text(self, text):
        model_id = "sentence-transformers/all-MiniLM-L6-v2"

        api_url = f"https://api-inference.huggingface.co/pipeline/feature-extraction/{model_id}"
        headers = {"Authorization": f"Bearer {hf_token}"}

        response = requests.post(
            api_url,
            headers=headers,
            json={"inputs": text, "options": {"wait_for_model": True}},
        )
        return response.json()
    

    def generate_answer(self, query: str, contexts: list[str]):
        print("huggingface access token: ", hf_token)

        device = "cuda" # the device to load the model onto

        model_name = "mistralai/Mistral-7B-Instruct-v0.2"
        model = AutoModelForCausalLM.from_pretrained("mistralai/Mistral-7B-Instruct-v0.2")
        tokenizer = AutoTokenizer.from_pretrained("mistralai/Mistral-7B-Instruct-v0.2")

        documents = ""
        for idx, context in enumerate(contexts):
            documents += f"\n\n Document {idx}: {context}\n"

        messages = [
            {"role": "user", "content": INSTRUCTION_PROMPT},
            {"role": "assistant", "content": "Well, I'm quite partial to a good squeeze of fresh lemon juice. It adds just the right amount of zesty flavour to whatever I'm cooking up in the kitchen!"},
            {"role": "user", "content": f"Query: {query}, Documents: {documents}"},
        ]


        encodeds = tokenizer.apply_chat_template(conversation=messages, return_tensors="pt")
        model_inputs = encodeds.to(device)
        model.to(device)

        generated_ids = model.generate(model_inputs, max_new_tokens=1000, do_sample=True)
        decoded = tokenizer.batch_decode(generated_ids)
        

        print(f"Contexts: {contexts}")

        return decoded[0]

            

    def get_relevant_docs(self, query: str):
        """ get relevant documents from the database """

        try:
            query_vector = self.query_text(query)

            print(f"Query vector: {query_vector}")

            # Get the collection
            formula1_data = self.client.collections.get("formula1")
            # Query the collection
            response = formula1_data.query.near_vector(
                near_vector=query_vector,
                # query_properties=["name", "location", "country"],
                limit=3,
                return_metadata=MetadataQuery(distance=True),
            )


            return [{"properties": o.properties} for o in response.objects] # [{"id": o.uuid, "properties": o.properties} for o in response.objects]
        except Exception as e:
            raise Exception(f"Could not get relevant documents: {str(e)}")


    # def get_movies(self, limit: int = 100):
    #     """ get movies from the database """
        
    #     try:
    #         movies = self.client.collections.get("Movies")
    #         response = movies.query.fetch_objects(limit=limit)
            
    #         return [{"id": o.uuid, "properties": o.properties} for o in response.objects]
    #     except Exception as e:
    #         raise Exception(f"Could not get movies: {str(e)}")
        

    # def get_movies(self, limit: int = 100, query: str = None):
    #     """ get movies from the database """
        
    #     try:
    #         movies = self.client.collections.get("Movies")
    #         if query:
    #             response = movies.query.bm25(
    #             query=query,
    #             query_properties=["title"],
    #             limit=limit
    #         )
    #         else:
    #             response = movies.query.fetch_objects(limit=limit)
                
    #         return [{"id": o.uuid, "properties": o.properties} for o in response.objects]
    #     except Exception as e:
    #         raise Exception(f"Could not get movies: {str(e)}")
    


    # def get_movie_by_id(self, id: str):
    #     """ get a movie by its id """

    #     try:
    #         movies = self.client.collections.get("Movies")
    #         movie = movies.query.fetch_object_by_id(id)

    #         return movie.properties
    #     except Exception as e:
    #         raise Exception(f"Could not get movie by id: {str(e)}")
        
    


    # def get_similar_movies(self, id: str, k: int = 4):
    #     """ get similar movies to the given movie title """

    #     try:
    #         movies = self.client.collections.get("Movies")
    #         movie_obj = movies.query.fetch_object_by_id(
    #             id,
    #             include_vector=True
    #         )

    #         query_vector = movie_obj.vector.get("default")

    #         response = movies.query.near_vector(
    #             near_vector=query_vector,
    #             limit=k,
    #             return_metadata=wq.MetadataQuery(distance=True)
    #         )

    #         return [{"id": o.uuid, "properties": o.properties} for o in response.objects]
    #     except Exception as e:
    #         raise Exception(f"Could not get similar movies: {str(e)}")
        
    
