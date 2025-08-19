import chromadb

client = chromadb.PersistentClient(path="./chromadb_npc")
collection = client.get_collection(name="npc_prompts")

results = collection.get()
print("IDs:", results["ids"])
print("Documents:", results["documents"])
print("Metadatas:", results["metadatas"])
