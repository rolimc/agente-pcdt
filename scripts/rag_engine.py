# -*- coding: utf-8 -*-
"""rag_engine.py

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1zGvggYppW1vtSu9shnWYNTKV-xkE-qZe
"""



# scripts/rag_engine.py

from langchain.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain.chains.combine_documents import create_stuff_documents_chain
import spacy
import os

# Carrega spaCy
nlp = spacy.load("pt_core_news_sm")

def extrair_keywords(texto):
    doc = nlp(texto)
    return list(set([ent.text for ent in doc.ents if len(ent.text) > 3]))

def reescrever_pergunta(pergunta, usar_llm=True):
    if not usar_llm:
        return pergunta
    try:
        llm = ChatOpenAI(temperature=0, model="gpt-3.5-turbo")
        prompt = f"""
Reescreva a pergunta abaixo de forma mais técnica, clara e compatível com os termos utilizados em documentos clínicos do SUS e no PCDT HIV:

\"{pergunta}\"
"""
        return llm.invoke(prompt).content.strip()
    except Exception as e:
        print(f"[!] Falha ao usar LLM para reescrever pergunta: {e}")
        return pergunta

def load_rag_engine(faiss_path: str):
    embeddings = OpenAIEmbeddings()

    # Carrega a base FAISS salva localmente
    vectorstore = FAISS.load_local(
        folder_path=faiss_path,
        embeddings=embeddings,
        allow_dangerous_deserialization=True  # necessário no Streamlit Cloud
    )

    retriever = vectorstore.as_retriever(search_kwargs={"k": 10})
    llm = ChatOpenAI(temperature=0, model="gpt-3.5-turbo")

    prompt_template = PromptTemplate(
        input_variables=["context", "pergunta"],
        template="""
Use the following pieces of context to answer the question at the end.
If you don't know the answer, just say that you don't know, don't try to make up an answer.
Use three sentences maximum and keep the answer as concise as possible.

{context}
Pergunta: {pergunta}
Resposta:
"""
    )

    chain = create_stuff_documents_chain(
        llm=llm,
        prompt=prompt_template,
        document_variable_name="context"
    )

    return chain, retriever, reescrever_pergunta
