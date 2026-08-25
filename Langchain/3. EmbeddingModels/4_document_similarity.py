from langchain_openai import OpenAIEmbeddings
from dotenv import load_dotenv
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

load_dotenv()

embedding = OpenAIEmbeddings(model='text-embedding-3-large', dimensions=300)

documents = [
    "Python is a popular programming language used for data science, machine learning, web development, and automation.",
    "Machine learning allows computers to learn patterns from data and make predictions without being explicitly programmed for every task.",
    "Deep learning is a subset of machine learning that uses neural networks with multiple layers to learn complex patterns from large datasets.",
    "Natural Language Processing, or NLP, enables computers to understand, process, and generate human language.",
    "Embeddings represent text as numerical vectors. Similar pieces of text tend to have vectors that are close together in vector space.",
    "Vector databases are designed to store and search high-dimensional vectors efficiently. They are commonly used for semantic search and retrieval-augmented generation.",
    "Retrieval-Augmented Generation combines information retrieval with a language model. Relevant documents are retrieved and provided to the model as context.",
    "Large language models are neural networks trained on huge amounts of text data. They can perform tasks such as answering questions, summarizing documents, and generating code.",
    "Artificial intelligence is a broad field focused on creating systems capable of performing tasks that normally require human intelligence.",   
    "Agentic AI systems can use tools, reason over intermediate steps, and take actions to accomplish a given goal."
]

query = "What are embeddings and how do they represent text?"



doc_embeddings = np.array(
    embedding.embed_documents(documents)
)

query_embedding = np.array(
    embedding.embed_query(query)
)

# Convert query from 1D -> 2D
query_embedding = query_embedding.reshape(1, -1)

scores = cosine_similarity(doc_embeddings, query_embedding).flatten()

results = sorted(
    enumerate(scores),
    key=lambda x: x[1],
    reverse=True
)

index = np.argmax(scores)

print(documents[index])