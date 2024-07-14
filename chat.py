from llama_cpp import Llama
from fastapi import FastAPI
from pydantic import BaseModel
from typing import List

app = FastAPI(title="Phi-3")

conversation_history: List[dict] = []


class Sentence(BaseModel):
    text: str = ""


def process(content, history):
    llm = Llama(
        model_path="/home/devuser/phi-3/Phi-3-mini-4k-instruct-q4.gguf",
        n_ctx=2048,
        n_threads=16,
        n_batch=2048,
        n_threads_batch=16,
        verbose=False
    )
    chat_input = history + [{"role": "user", "content": content}]
    chat = llm.create_chat_completion(
        messages=chat_input,
        max_tokens=2048,
        temperature=0,
    )
    output = chat["choices"][0]["message"]["content"]
    return output


@app.post('/chat')
async def chat(sentences: Sentence):
    global conversation_history
    output = process(sentences.text, conversation_history)

    # Update the conversation history
    conversation_history.append({"role": "user", "content": sentences.text})
    conversation_history.append({"role": "assistant", "content": output})

    return {'output': output}
