""" This retriever class gets data from weaviate and returns it to the user. """

import os
import requests
import weaviate
import weaviate.classes.query as wq
import weaviate.classes.config as wc
import pandas as pd
from typing import List, Union
from weaviate.classes.query import MetadataQuery
import openai
from openai import OpenAI

from transformers import AutoModelForCausalLM, AutoTokenizer
from dotenv import load_dotenv
load_dotenv()

hf_token = os.getenv("HUGGINGFACE_APIKEY")

client = OpenAI(
    # This is the default and can be omitted
    api_key=os.environ.get("OPENAI_API_KEY"),
)

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
    

    # def generate_answer(self, query: str, contexts: list[str]):
    #     print("huggingface access token: ", hf_token)

    #     device = "cuda" # the device to load the model onto

    #     # model_name = "mistralai/Mistral-7B-Instruct-v0.2"
    #     model = AutoModelForCausalLM.from_pretrained("mistralai/Mistral-7B-Instruct-v0.2", token=hf_token)
    #     tokenizer = AutoTokenizer.from_pretrained("mistralai/Mistral-7B-Instruct-v0.2")


    #     documents = ""
    #     for idx, context in enumerate(contexts):
    #         documents += f"\n\n Document {idx}: {context}\n"


    #     print("got here 2")

    #     messages = [
    #         {"role": "user", "content": INSTRUCTION_PROMPT},
    #         {"role": "assistant", "content": "Well, I'm quite partial to a good squeeze of fresh lemon juice. It adds just the right amount of zesty flavour to whatever I'm cooking up in the kitchen!"},
    #         {"role": "user", "content": f"Query: {query}, Documents: {documents}"},
    #     ]
        
    #      response = openai.ChatCompletion.create(
    #         engine = get_deployment_name(self.model_to_use),
    #         messages = messages,
    #         **self.control_parameters,
    #     )
    #     completion = response['choices'][0]['message']['content']


    def generate_answer(self, query: str, contexts: list[str]):
        print("Initial query:", query)

        # step 1: generate new query based on query + conversation history
        # new_query = query
        # if conversation_history is not None and len(conversation_history) > 0:
        #     new_query = self.generate_new_query(query=query, conversation_history=conversation_history)

        print("Query used for retrieval:", query)


        prompt = f"""Question: {query} + "\n" + Documents:" + \
        """

        for idx, document in enumerate(contexts):    
            prompt += f"""Document {idx + 1}
            
            {document}

        """
        
        # if conversation_history is not None:
        #     system_prompt += "\n\n You may use the previous messages to keep the context of the conversation."

        messages = [{"role": "system", "content": INSTRUCTION_PROMPT}]
        
        # add shots/samples to make sure model follows same format
        # messages.extend([
        #         {"role": "user", "content": SAMPLE_QUESTION},
        #         {"role": "assistant", "content": SAMPLE_ANSWER},
        # ])

        # # add conversation history
        # if conversation_history is not None:
        #     for message in conversation_history:
        #         messages.append({"role": "user", "content": "Previous message:" + message})
        
        # add query
        messages.append({"role": "user", "content": prompt})

        # num_tokens = num_tokens_from_messages(messages, model_name=self.model_to_use)
        # print("Number of message tokens before truncation:", num_tokens)

        # truncate messages
        # messages = truncate_messages(messages, max_tokens=self.control_parameters["max_tokens"], model_name=self.model_to_use)

        # num_tokens = num_tokens_from_messages(messages, model_name=self.model_to_use)
        # print("Number of message tokens after truncation:", num_tokens)

        print("Messages:", messages)

        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=messages,
            temperature=0.3,
            max_tokens=300
        )

        completion = response.choices[0].message.content

        return completion
            

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
        
    
