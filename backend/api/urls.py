from django.urls import path
from .views import ask_ai, get_books, get_book_detail

urlpatterns = [
    path('ask/', ask_ai, name='ask_ai'),
    path('books/', get_books, name='get_books'),
    path('books/<int:pk>/', get_book_detail, name='get_book_detail'),
]