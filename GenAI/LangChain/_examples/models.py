from langchain_ollama import OllamaLLM, ChatOllama
from langchain.chat_models import init_chat_model

from typing import Literal, Union, List
from pydantic import BaseModel, Field

from rich import print, print_json


class Initialize_Model:
    def __init__(self, 
                 model: Literal["deepseek-r1:14b", "llama3.2:latest", "qwen2.5:14b"] = "qwen2.5:14b", 
                 temperature: float = 0.3, 
                 num_ctx: int = 10000, 
                 num_predict: int = None, 
                 api_key: str = "SomethingSomething", 
                 format: str = None, 
                 verbose: bool = False):
        """
        Initialize an instance of the Initialize_Model class.

        Parameters:
        - model (str): The name of the model to be used. It can be either "deepseek-r1:14b-qwen-distill-q4_K_M" or "llama3.2:3b-instruct-fp16". The default value is "deepseek-r1:14b-qwen-distill-q4_K_M".
        - temperature (float): The temperature parameter for the model. The default value is 0.3.
        - num_ctx (int): The number of context tokens to be used. The default value is 10000.
        - num_predict (int): The number of tokens to predict. If not provided, it defaults to half of num_ctx.
        - api_key (str): The API key for accessing the OpenAI API. The default value is "SomethingSomething".
        - format (str): The format of the output. If not provided, it defaults to None.
        - verbose (bool): A flag indicating whether to print verbose output. The default value is False.

        Returns:
        - None
        """
        self.model = model
        self.temperature = temperature
        self.num_ctx = num_ctx
        self.num_predict = num_predict if num_predict is not None else self.num_ctx // 2  # Default to half of num_ctx
        self.api_key = api_key
        self.format = format
        self.verbose = verbose
        
        
    def Ollama_Model(self, base_url: str = "http://localhost:11434/") -> ChatOllama:
        
        try:
            # Initialize the client here
            self.model = ChatOllama(
                model=self.model,
                base_url=base_url,
                temperature=self.temperature,
                num_ctx=self.num_ctx,
                num_predict=self.num_predict,
                api_key=self.api_key,
                format=self.format,
                verbose=self.verbose,
            )

            return self.model

        except Exception as e:
            raise Exception(f"Failed to initialize model_name: {self.model_name}\nError: {str(e)}")
    

def main():
    
    local_model = Initialize_Model('qwen2.5:14b', temperature=2.5).Ollama_Model()
    # local_model = init_chat_model('ollama:qwen2.5:14b')

    result = local_model.invoke("Which city is hotter today and which is bigger: LA or NY?")

    print(result)

if __name__ == '__main__':
    main()