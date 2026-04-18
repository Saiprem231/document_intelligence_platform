from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Book
from .serializers import BookSerializer
from .services import get_ai_response

# 1. GET: List all books
@api_view(['GET'])
def get_books(request):
    books = Book.objects.all()
    serializer = BookSerializer(books, many=True)
    return Response(serializer.data)

# 2. GET: Retrieve specific book details
@api_view(['GET'])
def get_book_detail(request, pk):
    try:
        book = Book.objects.get(pk=pk)
        serializer = BookSerializer(book)
        return Response(serializer.data)
    except Book.DoesNotExist:
        return Response({"error": "Book not found"}, status=404)

# 3. POST: Ask the AI (RAG Pipeline with Memory)
@api_view(['POST'])
def ask_ai(request):
    question = request.data.get('question')
    history = request.data.get('history', []) # Catch the history, default to empty list
    
    if not question:
        return Response({"error": "Please provide a question."}, status=400)
    
    # Pass BOTH to your service
    result = get_ai_response(question, history)
    return Response(result)