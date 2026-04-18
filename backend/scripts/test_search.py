import chromadb

# 1. Connect to your local vector brain
chroma_client = chromadb.PersistentClient(path="./chroma_db")
collection = chroma_client.get_collection(name="books_collection")

# 2. The vague question we want the AI to understand
query = "I am looking for a dark, creepy psychological thriller."
print(f"Searching for: '{query}'...\n")

# 3. Query the database for the top 2 closest mathematical matches
results = collection.query(
    query_texts=[query],
    n_results=2 
)

# 4. Print the results
print("--- AI SEARCH RESULTS ---")
for i in range(len(results['documents'][0])):
    title = results['metadatas'][0][i]['title']
    distance = results['distances'][0][i]
    print(f"Match #{i+1}: {title}")
    print(f"Math Distance: {distance:.4f}")
    print("-" * 25)