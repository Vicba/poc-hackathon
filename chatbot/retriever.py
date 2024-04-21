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

        print("response: ", response.json())
        return response.json()
    



    def generate_answer(self, query: str, contexts: list[str]):

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

            # Get the collection
            formula1_data = self.client.collections.get("formula1")
            # Query the collection
            response = formula1_data.query.near_vector(
                near_vector=query_vector,
                # query_properties=["name", "location", "country"],
                # query=query,
                limit=1,
                # return_metadata=MetadataQuery(distance=True),
            )


            return [{"properties": o.properties} for o in response.objects] # [{"id": o.uuid, "properties": o.properties} for o in response.objects]
        except Exception as e:
            raise Exception(f"Could not get relevant documents: {str(e)}")