__import__("pysqlite3")
import sys

sys.modules["sqlite3"] = sys.modules.pop("pysqlite3")
import chromadb


client = chromadb.PersistentClient(path=".chroma_data")
collection = client.get_or_create_collection(
    name="vectorstore", metadata={"hnsw:space": "cosine"}
)
