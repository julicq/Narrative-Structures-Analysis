# service/llm.py

from langchain.llms import LlamaCpp
from langchain.callbacks.manager import CallbackManager
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler

def initialize_llm():
    callback_manager = CallbackManager([StreamingStdOutCallbackHandler()])
    
    llm = LlamaCpp(
        model_path="../models/llama/7B/ggml-model-q4_0.bin",
        callback_manager=callback_manager,
        verbose=True
    )
    
    return llm
