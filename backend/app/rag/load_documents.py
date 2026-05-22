from langchain_community.document_loaders import TextLoader
import os

DATA_PATH = "data"


def load_documents():
    documents = []

    for file in os.listdir(DATA_PATH):

        if file.endswith("tex"):

            loader = TextLoader(os.path.join(DATA_PATH, file))

            documents.extend(loader.load())

    return documents
