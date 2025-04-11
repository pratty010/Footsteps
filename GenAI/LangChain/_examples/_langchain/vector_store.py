from langchain_community.vectorstores import InMemoryVectorStore, FAISS,
from langchain_chroma.vectorstores import Chroma
from langchain_community.docstore.in_memory import InMemoryDocstore
from langchain_qdrant import QdrantVectorStore
from qdrant_client import QdrantClient
from qdrant_client.http.models import Distance, VectorParams

from langchain_core.documents import Document
from langchain_core.vectorstores import VectorStoreRetriever

from rich import print
from typing import Literal, Union, List, Dict

from _examples.embeddings import init_Google_embed, init_Ollama_embed
from _examples.loaders import file_loader
from _examples.splitters import rec_char_splitter

class Init_VS:
    """
    A class to initialize and manage different types of Vector Stores.
    """
    def __init__(
        self,
        embed_inst: Union[init_Google_embed, init_Ollama_embed],
        vs_type: Literal["InMemory", "Chroma", "Qdrant", "FAISS"] = "Chroma",
        ):
        """
        Initializes the Init_VS class.

        Args:
            embed_inst (Union[init_Google_embed, init_Ollama_embed]): An instance of the embedding model to be used.
            vs_type (Literal["InMemory", "Chroma", "Qdrant", "FAISS"], optional): The type of Vector Store to initialize. Defaults to "Chroma".
        """
        self.embed_inst = embed_inst
        self.vs_type = vs_type

    def __call__(
        self,
        **kwargs
        ) -> Union[InMemoryVectorStore, Chroma, QdrantVectorStore, FAISS]:
        """
        Initializes the Vector Store based on the specified type.

        Args:
            **kwargs: Keyword arguments specific to the Vector Store type.
        Returns:
            Union[InMemoryVectorStore, Chroma, QdrantVectorStore, FAISS]: An instance of the initialized Vector Store.
        Raises:
            ValueError: If an invalid Vector Store type is specified.
            Exception: If an error occurs during initialization.
        """

        try:
            if self.vs_type == "InMemory":
                # Initialize InMemoryVectorStore
                self.vs = InMemoryVectorStore(embedding=self.embed_inst)

            elif self.vs_type == "Chroma":
                # Initialize Chroma Vector Store
                self.vs = Chroma(
                    collection_name = kwargs.get("collection_name"),
                    embedding_function = self.embed_inst,
                    persist_directory = kwargs.get("persist_directory", None),
                    collection_metadata = kwargs.get('collection_metadata', None),
                    )

            elif self.vs_type == "FAISS":
                # Initialize FAISS Vector Store
                self.vs = FAISS(
                    embedding_function=self.embedding_model,
                    index=kwargs.get("index"),
                    docstore=kwargs.get("docstore", InMemoryDocstore()),
                    index_to_docstore_id=kwargs.get("index_to_docstore_id",{}),
                )

            elif self.vs_type == "Qdrant":
                # Initialize Qdrant Vector Store
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

            else:
                raise ValueError("Invalid Vector Store type. Supported types are 'InMemory', 'Chroma', 'Qdrant', 'FAISS'.")

            return self.vs

        except Exception as e:
            raise f"Error while initializing {type}: {e}"

    def add_documents(
        self,
        documents: List[Document],
        ids: List[str] = None,
        vs: Union[InMemoryVectorStore, Chroma, QdrantVectorStore, FAISS] = None,
        ) -> List[str]:
        """
        Adds a list of documents to the Vector Store.

        Parameters:
        - documents (list[Document]): A list of Document objects to be added to the Vector Store.
        - ids (list[str], optional): A list of unique identifiers for the documents. If not provided, the Vector Store will generate unique identifiers.
        - vs (Union[InMemoryVectorStore, Chroma, QdrantVectorStore, FAISS], optional): An instance of the Vector Store to add the documents to. If not provided, the documents will be added to the default Vector Store.

        Returns:
        - list[str]: A list of unique identifiers assigned to the added documents.

        Raises:
        - Exception: If an error occurs while adding the documents to the Vector Store.
        """
        try:
            if vs:
                # Add documents to the provided Vector Store instance
                results = vs.add_documents(documents=documents, ids=ids)
            else:
                # Add documents to the default Vector Store instance
                results = self.vs.add_documents(documents=documents, ids=ids)

            return results
        except Exception as e:
            raise f"Error adding documents to VS: {e}"

    def add_texts(
        self,
        texts: List[str],
        metadatas: List[Dict] = None,
        ids: List[str] = None,
        vs:  Union[InMemoryVectorStore, Chroma, QdrantVectorStore, FAISS] = None,
        ) -> List[str]:
        """
        Adds a list of texts to the Vector Store.

        Parameters:
        - texts (list[str]): A list of text strings to be added to the Vector Store.
        - metadatas (list[dict], optional): A list of metadata dictionaries associated with the texts. If not provided, default metadata will be used.
        - ids (list[str], optional): A list of unique identifiers for the texts. If not provided, the Vector Store will generate unique identifiers.
        - vs (Union[InMemoryVectorStore, Chroma, QdrantVectorStore, FAISS], optional): An instance of the Vector Store to add the texts to. If not provided, the texts will be added to the default Vector Store.

        Returns:
        - list[str]: A list of unique identifiers assigned to the added texts.

        Raises:
        - Exception: If an error occurs while adding the texts to the Vector Store.
        """
        try:
            if vs:
                # Add texts to the provided Vector Store instance
                results = vs.add_texts(texts=texts, metadatas=metadatas, ids=ids)
            else:
                # Add texts to the default Vector Store instance
                results = self.vs.add_texts(texts=texts, metadatas=metadatas, ids=ids)

            return results
        except Exception as e:
            raise f"Error adding texts to VS: {e}"

    def delete_documents(
        self,
        ids: List[str] = None,
        vs: Union[InMemoryVectorStore, Chroma, QdrantVectorStore, FAISS] = None
        ) -> None:
        """
        Deletes documents from the Vector Store based on the provided unique identifiers.

        Parameters:
        - ids (list[str], optional): A list of unique identifiers for the documents to be deleted. If not provided, all documents in the Vector Store will be deleted.
        - vs (Union[InMemoryVectorStore, Chroma, QdrantVectorStore, FAISS], optional): An instance of the Vector Store from which the documents will be deleted. If not provided, the deletion will be performed on the default Vector Store.

        Returns:
        - None: The function does not return any value.

        Raises:
        - Exception: If an error occurs while deleting the documents from the Vector Store.
        """
        try:
            if vs:
                # Delete documents from the provided Vector Store instance
                vs.delete(ids=ids)
            else:
                # Delete documents from the default Vector Store instance
                self.vs.delete(ids=ids)
                
        except Exception as e:
            raise f"Error deleting documents to VS: {e}"

    def get_vs_retriever(
        self,
        vs: Union[InMemoryVectorStore, Chroma, QdrantVectorStore, FAISS] = None,
        search_type: str="similarity",
        search_kwargs: dict= {"k": 2}
        ) -> VectorStoreRetriever:
        """
        Creates and returns a retriever instance from the specified Vector Store.

        Parameters:
        - vs (Union[InMemoryVectorStore, Chroma, QdrantVectorStore, FAISS, optional): The Vector Store instance from which the retriever will be created. If not provided, the default Vector Store will be used.
        - search_type (str, optional): The type of search to perform. Can be either "similarity" or "embedding". Default is "similarity".
        - search_kwargs (dict, optional): Additional keyword arguments to be passed to the search method.

        Returns:
        - VectorStoreRetriever: An instance of VectorStoreRetriever that can be used to retrieve documents based on queries.

        Raises:
        - Exception: If an error occurs while creating the retriever.
        """
        try:
            if vs:
                # Create retriever from the provided Vector Store instance
                return vs.as_retriever(
                    search_type=search_type,
                    search_kwargs=search_kwargs,
                    )
            else:
                # Create retriever from the default Vector Store instance
                return self.vs.as_retriever(
                    search_type=search_type,
                    search_kwargs=search_kwargs,
                    )

        except Exception as e:
            raise f"Error creating VS retriever: {e}"


def main():

    # Initialize the Embeddings Model of choice
    # ollama_embed = init_Ollama_embed()
    google_embed = init_Google_embed(task_type='retrieval_document')
    
    # # Initialize the Vector Store Model with proper embeddings.
    vs_model = Init_VS(google_embed, 'Chroma')

    # # Initialize the Vector Store
    # vs = vs_model()
    vs = vs_model(
        collection_name="Langchain",
        persist_directory="./_data/vectorstore/chroma"
        )
    # print(vs)

    # Add documents to the Vector Store
    data = file_loader('./_data/_sample/sample.txt')
    docs = rec_char_splitter(data, 'split-docs', chunk_overlap=20, chunk_size=200)
    # print(docs)
    
    ids = vs_model.add_documents(docs, vs=vs)
    # print(ids)

    query = "What is Anthropic?"
    print(vs.similarity_search(query, k=4))
    ret = vs_model.get_vs_retriever()
    print(ret.invoke('2'))


if __name__ == "__main__":
    main()