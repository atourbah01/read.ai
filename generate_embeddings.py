import pandas as pd
from sentence_transformers import SentenceTransformer
import chromadb
from chromadb.config import Settings

# Load the dataset
df = pd.read_csv('books.csv')

# Create combined text field
df['combined_text'] = df['title'] + ' by ' + df['author'] + '. ' + df['genres'] + '. ' + df['summary']

# Load the model
model = SentenceTransformer('all-MiniLM-L6-v2')

# Generate embeddings
embeddings = model.encode(df['combined_text'].tolist())

# Initialize ChromaDB
client = chromadb.PersistentClient(path="./chroma_db")

# Create or get collection
collection = client.get_or_create_collection(name="books")

# Add documents
collection.add(
    embeddings=embeddings.tolist(),
    documents=df['combined_text'].tolist(),
    metadatas=df[['title', 'author', 'genres', 'summary']].to_dict('records'),
    ids=df.index.astype(str).tolist()
)

print("Embeddings generated and stored in ChromaDB.")