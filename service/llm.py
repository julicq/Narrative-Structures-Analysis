# service/llm.py

from langchain.llms import Ollama
from langchain.callbacks.manager import CallbackManager
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler

def initialize_llm():
    callback_manager = CallbackManager([StreamingStdOutCallbackHandler()])
    
    llm = Ollama(
        model="llama3.2",  # Используем модель llama3.2
        callback_manager=callback_manager,
        verbose=True
    )
    
    return llm
