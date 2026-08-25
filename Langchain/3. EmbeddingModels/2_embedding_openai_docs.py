from langchain_openai import OpenAIEmbeddings
from dotenv import load_dotenv

load_dotenv()

embedding = OpenAIEmbeddings(model='text-embedding-3-small', dimensions=32)

documents = [
    'Delhi is the capital of India',
    'Kolkata is the capital of India',
    'Paris is the captial of France'
]

result = embedding.embed_documents(documents)

print(str(result))