import os
from git import Repo
from langchain.document_loaders.generic import GenericLoader
from langchain.document_loaders.parsers import LanguageParser
from langchain.text_splitter import Language
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain_community.embeddings import GPT4AllEmbeddings
import chromadb.utils.embedding_functions as embedding_functions
from dotenv import load_dotenv

load_dotenv()

HUGGINGFACE_API_KEY = os.environ.get('HUGGINGFACE_API_KEY')
os.environ["HUGGINGFACE_API_KEY"] = HUGGINGFACE_API_KEY

# Cloning Repos
def repo_ingestion(repo_url):
    os.makedirs("repo", exist_ok=True)
    repo_path= "repo/"
    Repo.clone_from(repo_url, to_path=repo_path)


def load_repo(repo_path):
    loader = GenericLoader.from_filesystem(repo_path,
                                           glob="**/*",
                                           suffixes=[".py"],
                                           parser=LanguageParser
                                           (language=Language.PYTHON, 
                                           ))
    docouments =loader.load()
    return docouments

# Chunking 

def text_splitter(documents):
    documents_splitter = RecursiveCharacterTextSplitter.from_language(language = Language.PYTHON,
                                                             chunk_size = 2000,
                                                             chunk_overlap = 200)
    text_chunks= documents_splitter.split_documents(documents)

    return text_chunks

def load_embedding(text):
    embeddings = embedding_functions.HuggingFaceEmbeddingFunction(
    api_key=HUGGINGFACE_API_KEY,
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)
    # gpt4all_embd = GPT4AllEmbeddings()
    # embeddings= gpt4all_embd.embed_documents()
    # embeddings=OpenAIEmbeddings(disallowed_special=())
    return embeddings

"""
huggingface_ef = embedding_functions.HuggingFaceEmbeddingFunction(
    api_key="YOUR_API_KEY",
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)
"""