# -*- coding: utf-8 -*-
"""feedback_utils.py

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/10PsnHmGCkeoVg0MlnchsOg8Bh7Y5l4Fg
"""

# scripts/feedback_utils.py

from langchain.vectorstores import Chroma
from langchain.embeddings import OpenAIEmbeddings
from langchain.schema import Document
import datetime

def load_feedback_vectorstore(chroma_path: str):
    embeddings = OpenAIEmbeddings()
    return Chroma(
        persist_directory=chroma_path,
        embedding_function=embeddings,
        collection_name="feedback"
    )

def salvar_feedback(feedback_store, pergunta, resposta_sugerida, especialista_id):
    metadata = {
        "especialista_id": especialista_id,
        "data": datetime.datetime.now().isoformat(),
        "tipo": "sugestao",
        "score": 1  # inicia com score 1
    }

    doc = Document(
        page_content=resposta_sugerida,
        metadata=metadata
    )
    feedback_store.add_documents([doc])
    feedback_store.persist()