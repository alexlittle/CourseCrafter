import os
import ssl
import http
import requests
import socket
import urllib3
from urllib import error

from django.conf import settings
from langchain_huggingface.embeddings import HuggingFaceEmbeddings
from langchain_core.runnables import RunnablePassthrough
from langchain_chroma import Chroma
from langchain_ollama.llms import OllamaLLM
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser, JsonOutputParser
from langchain.prompts import PromptTemplate
from langchain_community.document_loaders import WebBaseLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_google_genai import ChatGoogleGenerativeAI

BASE_DIR = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))

class CourseCrafterAI():

    vs = None
    llm = None
    llm_engine = settings.CRAFTER_CHAT_ENGINE
    llm_engine_model = settings.CRAFTER_CHAT_ENGINE_MODEL
    embedding_model = settings.CRAFTER_EMBEDDING_MODEL
    vs_data_dir = os.path.join(BASE_DIR, "datastore")
    chunk_size = 5000
    chunk_overlap = 1250

    def __init__(self, collection_name):

        self.vs = Chroma(
            collection_name=collection_name,
            embedding_function=HuggingFaceEmbeddings(model_name=self.embedding_model),
            persist_directory=self.vs_data_dir
        )

    def load_url(self,url):
        try:
            loader = WebBaseLoader(web_paths=(url,), )
            docs = loader.load()
            text_splitter = RecursiveCharacterTextSplitter(chunk_size=self.chunk_size, chunk_overlap=self.chunk_overlap)
            splits = text_splitter.split_documents(docs)

            return True, splits
        except (ssl.CertificateError,
                http.client.RemoteDisconnected,
                ConnectionResetError,
                socket.timeout,
                http.client.BadStatusLine,
                error.URLError,
                error.HTTPError,
                requests.exceptions.ConnectTimeout,
                socket.gaierror,
                urllib3.exceptions.NameResolutionError,
                urllib3.exceptions.ProtocolError,
                requests.exceptions.ConnectionError):
            print("failed to connect to {}".format(url))
            return False, None

    def init_chat(self, temperature=0.7):
        if self.llm_engine == "openai":
            if not os.environ.get("OPENAI_API_KEY"):
                os.environ["OPENAI_API_KEY"] = settings.OPENAI_API_KEY
            self.llm =  ChatOpenAI(model=self.llm_engine_model, temperature=temperature)
        elif self.llm_engine == "google-genai":
            if "GOOGLE_API_KEY" not in os.environ:
                os.environ["GOOGLE_API_KEY"] = settings.GOOGLE_GEN_AI_API_KEY
            self.llm = ChatGoogleGenerativeAI(model=self.llm_engine_model, temperature=temperature)
        else:
            self.llm = OllamaLLM(model=self.llm_engine_model, temperature=temperature)

    def get_vs(self):
        return self.vs

    def get_prompt_template(self, template):
        template_file = os.path.join(BASE_DIR,'prompttemplates/') + template + ".txt"
        with open(template_file, 'r') as file:
            return file.read()

    def format_docs(self, docs):
        return "\n\n".join(doc.page_content for doc in docs)

    def query(self, question, template='course_outline'):

        rag_prompt = PromptTemplate.from_template(self.get_prompt_template(template))

        retriever = self.vs.as_retriever(search_kwargs={"k": 100})

        rag_chain = (
                {"context": retriever | self.format_docs, "question": RunnablePassthrough()}
                | rag_prompt
                | self.llm
                | JsonOutputParser()
        )

        return rag_chain.invoke(question)
