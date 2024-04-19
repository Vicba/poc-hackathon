import logging
from datetime import datetime
from typing import Union
import os

import openai
from openai import OpenAI
import pandas as pd
from tenacity import retry, stop_after_delay, wait_fixed

client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
assistant = "gpt-4-0125-preview"
assistant_id = ""
logger = logging.getLogger(__name__)


def gpt_workflow(message: str):

    def create_thread():
        thread = client.beta.threads.create(
            messages=[]
        )
        thread_id = thread.id
        return thread_id

    def create_message(thread_id: str, content: str):
        message = client.beta.threads.messages.create(
            thread_id=thread_id,
            role="user",
            content=content
        )
        return message

    def create_run(thread_id: str):
        run = client.beta.threads.runs.create(
            assistant_id=assistant_id,
            thread_id=thread_id
        )
        run_id = run.id
        return run_id

    def wait_for_run_completion(thread_id, run_id):
        """
        args: thread_id: str, run_id: str
        Wait for the run to complete.
        return: response: str
        """
        while True:
            try:
                run = client.beta.threads.runs.retrieve(
                    thread_id=thread_id,
                    run_id=run_id
                )
                if run.status == "completed":
                    messages = client.beta.threads.messages.list(
                        thread_id=thread_id
                    )
                    last_message = messages.data[0]
                    response = last_message.content[0].text.value
                    return response
            except Exception as e:
                logger.error(e)
                raise e

    thread_id = create_thread()
    message = create_message(thread_id, message)
    run_id = create_run(thread_id)
    response = wait_for_run_completion(thread_id, run_id)
    return response
