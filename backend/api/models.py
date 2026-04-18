from django.db import models

class Book(models.Model):
    title = models.CharField(max_length=500)
    author = models.CharField(max_length=255)
    rating = models.CharField(max_length=50, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    book_url = models.URLField(unique=True, max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
