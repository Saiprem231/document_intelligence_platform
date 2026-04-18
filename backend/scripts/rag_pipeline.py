from openai import OpenAI
import chromadb

# 1. Connect to your local Vector Brain (ChromaDB)
chroma_client = chromadb.PersistentClient(path="./chroma_db")
collection = chroma_client.get_collection(name="books_collection")

# 2. Connect to Groq's FREE Cloud Brain
# Replace the string below with your real API key!
client = OpenAI(
    base_url="https://api.groq.com/openai/v1",
    api_key="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" 
)

def ask_document_intelligence(question):
    print(f"User: {question}")
    print("Thinking...\n")
    
    # A. RETRIEVE: Ask ChromaDB to find the most relevant book data
    results = collection.query(query_texts=[question], n_results=1)
    
    retrieved_context = results['documents'][0][0]
    book_title = results['metadatas'][0][0]['title']
    
    # B. AUGMENT: Combine the retrieved data with the user's question
    system_prompt = """
    You are an intelligent bookstore assistant. 
    You must answer the user's question using ONLY the provided context. 
    If the answer is not in the context, say you don't know.
    """
    
    user_message = f"Context from database: {retrieved_context}\n\nUser Question: {question}"
    
    # C. GENERATE: Send the packaged prompt to Groq's servers
    response = client.chat.completions.create(
        model="llama-3.1-8b-instant", # Groq's lightning-fast, free Llama 3 model
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_message}
        ],
        temperature=0.7
    )
    
    # D. Deliver the final insight
    print(f"[Data Retrieved From: {book_title}]")
    print(f"AI Assistant: {response.choices[0].message.content}\n")

# --- Let's test the full architecture! ---
user_query = "I'm looking for a dark psychological thriller. What do you recommend and what is the plot?"
ask_document_intelligence(user_query)