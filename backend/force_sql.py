import os
import django

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from django.db import connection

# The raw SQL to build your table exactly how the scraper expects it
raw_sql = """
CREATE TABLE IF NOT EXISTS api_book (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(500) NOT NULL,
    author VARCHAR(255) NOT NULL,
    rating VARCHAR(50) NULL,
    description LONGTEXT NULL,
    book_url VARCHAR(500) NOT NULL UNIQUE,
    created_at DATETIME(6) NOT NULL
);
"""

# Force the command directly into MySQL
with connection.cursor() as cursor:
    cursor.execute(raw_sql)

print("SUCCESS: Table forcefully created in MySQL via direct SQL injection!")