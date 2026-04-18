import os

# Create the correct folders
os.makedirs("api/migrations", exist_ok=True)

# Create the required hidden Python files
with open("api/__init__.py", "w") as f: pass
with open("api/migrations/__init__.py", "w") as f: pass

# Write a perfectly clean apps.py
with open("api/apps.py", "w", encoding="utf-8") as f:
    f.write("from django.apps import AppConfig\n\nclass ApiConfig(AppConfig):\n    default_auto_field = 'django.db.models.BigAutoField'\n    name = 'api'\n")

# Write a perfectly clean models.py
with open("api/models.py", "w", encoding="utf-8") as f:
    f.write("from django.db import models\n\nclass Book(models.Model):\n    title = models.CharField(max_length=500)\n    author = models.CharField(max_length=255)\n    rating = models.CharField(max_length=50, null=True, blank=True)\n    description = models.TextField(null=True, blank=True)\n    book_url = models.URLField(unique=True, max_length=500)\n    created_at = models.DateTimeField(auto_now_add=True)\n\n    def __str__(self):\n        return self.title\n")

print("Clean files generated successfully! Django can now read your code.")