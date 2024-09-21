import os
import openai
from langchain_community.embeddings import OpenAIEmbeddings
from langchain_core.prompts import PromptTemplate
from langchain.chains import ConversationalRetrievalChain
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_community.llms import OpenAI

model = OpenAI(
    openai_api_key=OPENAI_API_KEY,)

pdf_reader = PyPDFLoader("./assets/website_cost_quotation.pdf")
document = pdf_reader.load()
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000, chunk_overlap=200)
chunks = text_splitter.split_documents(document)

embeddings = OpenAIEmbeddings(api_key=OPENAI_API_KEY)
db = FAISS.from_documents(documents=chunks, embedding=embeddings)

CONDENSE_QUESTION_PROMPT = PromptTemplate.from_template(
    """Given the context below, rewrite the question to be asked in simpler terms.
    Chat History: {chat_history}
    Follow up Input: {question}hosting
    standalone question:""")

qa = ConversationalRetrievalChain.from_llm(
    llm=model,
    retriever=db.as_retriever(),
    condense_question_prompt=CONDENSE_QUESTION_PROMPT,
    return_source_documents=True,
    verbose=False
)

chat_history = []
question = "What is the cost of building a ecommerce website with Admin dashboard?"
result = qa({"question": question, "chat_history": chat_history})
print(result)
