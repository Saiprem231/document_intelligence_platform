import hashlib
from django.core.cache import cache
from openai import OpenAI
import chromadb

# Connect to your Vector Brain
chroma_client = chromadb.PersistentClient(path="./chroma_db")
collection = chroma_client.get_collection(name="books_collection")

# Connect to Groq Cloud
client = OpenAI(
    base_url="https://api.groq.com/openai/v1",
    api_key="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"  # <-- Paste your real key here!
)

def get_ai_response(question, history=[]):
    # --- CACHE CHECK ---
    # Only hash the lowercase question so history doesn't break the cache match
    fingerprint_string = question.strip().lower()
    cache_key = "rag_" + hashlib.md5(fingerprint_string.encode('utf-8')).hexdigest()
    
    cached_result = cache.get(cache_key)
    if cached_result:
        # If found in DB, return it instantly and add a flag to prove it works
        cached_result['answer'] = "⚡ [CACHED RESPONSE] " + cached_result['answer']
        return cached_result

    # --- 1. Retrieve ---
    results = collection.query(query_texts=[question], n_results=1)
    
    if not results['documents'][0]:
        return {"answer": "I couldn't find any relevant books in the database.", "source": "None"}

    retrieved_context = results['documents'][0][0]
    book_title = results['metadatas'][0][0]['title']
    
    # --- 2. Augment System Prompt ---
    system_prompt = """
    You are an intelligent bookstore assistant. 
    You must answer the user's question using the provided context and previous conversation. 
    CRITICAL INSTRUCTION: You must ALWAYS respond in the same language as the User Question. If the user asks in English, you must reply in English, even if the database context contains French or other languages.
    If the answer is not in the context, politely inform the user that there are no books matching their request in the current library. Do NOT mention the specific context you were provided in your refusal.
    """
    
    # --- 3. Build Conversational Memory ---
    messages = [{"role": "system", "content": system_prompt}]
    for msg in history:
        messages.append({"role": msg['role'], "content": msg['content']})
        
    user_message = f"Context from database: {retrieved_context}\n\nUser Question: {question}"
    messages.append({"role": "user", "content": user_message})
    
    # --- 4. Generate ---
    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=messages,
        temperature=0.7
    )
    
    final_result = {
        "answer": response.choices[0].message.content,
        "source": book_title
    }
    
    # --- CACHE SAVE ---
    # Save the successful result to the database for 24 hours (86400 seconds)
    cache.set(cache_key, final_result, 86400)
    
    return final_result