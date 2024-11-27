from .models import Book
from rest_framework import serializers

class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = '__all__'
        swagger_schema_fields = {
            'example': {
                'title': 'John Doe',
                'page_count': 30,
                'isbn': "1234567890abc"
            }
        }