from langchain_chroma.vectorstores import Chroma
from langchain_community.vectorstores import InMemoryVectorStore, FAISS
from langchain_chroma import Chroma
from langchain_community.docstore.in_memory import InMemoryDocstore
from langchain_qdrant import QdrantVectorStore
from qdrant_client import QdrantClient
from qdrant_client.http.models import Distance, VectorParams

from langchain_core.documents import Document

from rich import pretty, print
from typing import Literal, Union

from _tools._lang.embeddings import CreateOllamaEmbeddings

class CreateVS:
    def __init__(self, embedding_model: str):
        """
        Initialize an instance of ChromaVS or InMemoryVS with a specified embedding model.

        Parameters:
        - embedding_model (str): The name or path of the embedding model to be used for document embeddings.

        Attributes:
        - self.embedding_model (str): The name or path of the embedding model used for document embeddings.
        """
        self.embedding_model = embedding_model

    def __call__(self, type: Literal["InMemory", "Chroma", "Qdrant", "FAISS"] = "Chroma", **kwargs) -> Union[InMemoryVectorStore, Chroma, QdrantVectorStore, FAISS]:
        """
        Initializes and returns a Vector Store instance based on the provided type and keyword arguments.

        Parameters:
        - type (str): The type of Vector Store to initialize. Supported types are 'InMemory', 'Chroma', 'Qdrant', 'FAISS'. Default is 'Chroma'.
        - kwargs (dict): Additional keyword arguments specific to the chosen Vector Store type.

        Returns:
        - Union[InMemoryVectorStore, Chroma, QdrantVectorStore, FAISS]: An instance of the initialized Vector Store.

        Raises:
        - Exception: If an error occurs during initialization.
        """
        try:
            if type == "InMemory":
                self.vs = InMemoryVectorStore(embedding=self.embedding_model)

            elif type == "Chroma":
                self.vs = Chroma(
                    collection_name=kwargs.get("collection_name"),
                    embedding_function=self.embedding_model,
                    persist_directory=kwargs.get("persist_directory", None),
                    )
                
            elif type == "Qdrant":
                client = QdrantClient(path=kwargs.get("path"))

                if client.collection_exists(kwargs.get('collection_name')):
                    print(f"Collection {kwargs.get('collection_name')} already exists. Moving on.")
                else:
                    print(f"Creating collection {kwargs.get('collection_name')}.")
                    client.create_collection(
                        collection_name=kwargs.get("collection_name"),
                        vectors_config=VectorParams(
                            size=kwargs.get("size", 5120),
                            distance=kwargs.get("distance", Distance.COSINE),
                            ),
                    )
                self.vs = QdrantVectorStore(
                    client=client,
                    collection_name=kwargs.get("collection_name"),
                    embedding=self.embedding_model,
                )

            elif type == "FAISS":
                self.vs = FAISS(
                    embedding_function=self.embedding_model,
                    index=kwargs.get("index"),
                    docstore=kwargs.get("docstore", InMemoryDocstore()),
                    index_to_docstore_id=kwargs.get("index_to_docstore_id",{}),
                )

            else:
                raise ValueError("Invalid Vector Store type. Supported types are 'InMemory', 'Chroma', 'Qdrant', 'FAISS'.")

            return self.vs

        except Exception as e:
            print(f"Error while initializing {type}: {str(e)}")
            return None

    def add_documents(self,  documents: list[Document], ids: list[str] = None, vs: InMemoryVectorStore = None) -> list[str]:
        """
        Adds a list of documents to the Vector Store.

        Parameters:
        - documents (list[Document]): A list of Document objects to be added to the Vector Store.
        - ids (list[str], optional): A list of unique identifiers for the documents. If not provided, the Vector Store will generate unique identifiers.
        - vs (InMemoryVectorStore, optional): An instance of the InMemoryVectorStore to add the documents to. If not provided, the documents will be added to the default Vector Store.

        Returns:
        - list[str]: A list of unique identifiers assigned to the added documents.

        Raises:
        - Exception: If an error occurs while adding the documents to the Vector Store.
        """
        try:
            if vs:
                results = vs.add_documents(documents=documents, ids=ids)
            else:
                results = self.vs.add_documents(documents=documents, ids=ids)

            return results
        except Exception as e:
            print(f"Error adding documents to VS: {e}")
            return []

    def add_texts(self, texts: list[str], metadatas: list[dict] = None, ids: list[str] = None, vs: InMemoryVectorStore = None) -> list[str]:
        """
        Adds a list of texts to the Vector Store.

        Parameters:
        - texts (list[str]): A list of text strings to be added to the Vector Store.
        - metadatas (list[dict], optional): A list of metadata dictionaries associated with the texts. If not provided, default metadata will be used.
        - ids (list[str], optional): A list of unique identifiers for the texts. If not provided, the Vector Store will generate unique identifiers.
        - vs (InMemoryVectorStore, optional): An instance of the InMemoryVectorStore to add the texts to. If not provided, the texts will be added to the default Vector Store.

        Returns:
        - list[str]: A list of unique identifiers assigned to the added texts.

        Raises:
        - Exception: If an error occurs while adding the texts to the Vector Store.
        """
        try:
            if vs:
                results = vs.add_texts(texts=texts, metadatas=metadatas, ids=ids)
            else:
                results = self.vs.add_texts(texts=texts, metadatas=metadatas, ids=ids)

            return results
        except Exception as e:
            print(f"Error adding texts to VS: {e}")
            return []
        
    def delete_documents(self, ids: list[str] = None, vs: InMemoryVectorStore = None) -> None:
        """
        Deletes documents from the Vector Store based on the provided unique identifiers.

        Parameters:
        - ids (list[str], optional): A list of unique identifiers for the documents to be deleted. If not provided, all documents in the Vector Store will be deleted.
        - vs (InMemoryVectorStore, optional): An instance of the InMemoryVectorStore from which the documents will be deleted. If not provided, the deletion will be performed on the default Vector Store.

        Returns:
        - None: The function does not return any value.

        Raises:
        - Exception: If an error occurs while deleting the documents from the Vector Store.
        """
        try:
            if vs:
                results = vs.delete(ids=ids)
            else:
                results = self.vs.delete(ids=ids)
        except Exception as e:
            print(f"Error deleting documents to VS: {e}")
            return []

    def get_vs_retriever(self, vs: InMemoryVectorStore = None, search_type: str="similarity", search_kwargs: dict= {"k": 2}):
        """
        Creates and returns a retriever instance from the specified Vector Store.

        Parameters:
        - vs (InMemoryVectorStore, optional): The Vector Store instance from which the retriever will be created. If not provided, the default Vector Store will be used.
        - k (int, optional): The number of nearest neighbors to return for each query. Default is 5.
        - search_type (str, optional): The type of search to perform. Can be either "similarity" or "embedding". Default is "similarity".
        - search_kwargs (dict, optional): Additional keyword arguments to be passed to the search method.

        Returns:
        - Retriever: An instance of Retriever that can be used to retrieve documents based on queries.

        Raises:
        - Exception: If an error occurs while creating the retriever.
        """
        try:
            if vs:
                return vs.as_retriever(
                    search_type=search_type,
                    search_kwargs=search_kwargs,
                    )
            else:
                return self.vs.as_retriever(
                    search_type=search_type,
                    search_kwargs=search_kwargs,
                    )

        except Exception as e:
            print(f"Error creating VS retriever: {e}")


def main():

    # Initialize the Ollama Embeddings Model
    ollama_embed = CreateOllamaEmbeddings()

    # Initialize the Vector Store Model
    vs_model = CreateVS(embedding_model=ollama_embed())

    # Initialize the Vector Store
    # vs = vs_model(type="InMemory")
    vs = vs_model("Chroma", collection_name="test", persist_directory="./_data/vectorstore/chroma")

    print(vs)

    # # Add documents to the Vector Store
    # documents = [
    #     Document(id = 1, page_content="Document 1 content"),
    #     Document(id = 2, page_content="Document 2 content"),
    #     Document(id = 3, page_content="Document 3 content"),
    # ]
    
    # ids = vs_model.add_documents(documents)
    # print(ids)

    # print(vs.similarity_search_with_score('2'))
    # ret = vs_model.get_vs_retriever()
    # print(ret.invoke('2'))


if __name__ == "__main__":
    main()