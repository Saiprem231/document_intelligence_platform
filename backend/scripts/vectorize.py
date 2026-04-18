import os
import sys
import django
import chromadb

# --- THE MAGIC BRIDGE ---
# Tell Python to look in the parent directory (backend) for Django files
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# 1. Setup Django so we can safely read from your MySQL database
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from api.models import Book

print("Spinning up Vector Database...")
# 2. Initialize ChromaDB (This creates a physical folder in your backend to store the math)
chroma_client = chromadb.PersistentClient(path="./chroma_db")

# 3. Create a collection (ChromaDB's version of a 'table')
collection = chroma_client.get_or_create_collection(name="books_collection")

# 4. Fetch your scraped books from MySQL
books = Book.objects.all()
print(f"Found {books.count()} books in MySQL. Generating AI embeddings now...")

documents = []
metadatas = []
ids = []

for book in books:
    # We combine the title, author, and description into one "document" for the AI to read
    content = f"Title: {book.title}\nAuthor: {book.author}\nDescription: {book.description}"
    documents.append(content)
    
    # Metadata lets us filter the results later
    metadatas.append({
        "title": book.title,
        "url": book.book_url
    })
    
    # Chroma requires a unique string ID for every vector
    ids.append(str(book.id))

# 5. Inject the vectors into ChromaDB
if documents:
    collection.add(
        documents=documents,
        metadatas=metadatas,
        ids=ids
    )
    print("SUCCESS: Books have been vectorized and stored in ChromaDB!")
else:
    print("No books found to vectorize. Did you run the scraper?")