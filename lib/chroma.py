import chromadb


client = chromadb.PersistentClient(path="tes")
collection = client.get_or_create_collection(
    name="vectorstore", metadata={"hnsw:space": "cosine"}
)
