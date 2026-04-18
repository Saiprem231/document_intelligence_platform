import os

migration_code = """from django.db import migrations, models

class Migration(migrations.Migration):
    initial = True
    dependencies = []
    operations = [
        migrations.CreateModel(
            name='Book',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=500)),
                ('author', models.CharField(max_length=255)),
                ('rating', models.CharField(blank=True, max_length=50, null=True)),
                ('description', models.TextField(blank=True, null=True)),
                ('book_url', models.URLField(max_length=500, unique=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
"""

os.makedirs("api/migrations", exist_ok=True)
with open("api/migrations/0001_initial.py", "w", encoding="utf-8") as f:
    f.write(migration_code)

print("Blueprint physically forced into the folder! Django MUST read it now.")