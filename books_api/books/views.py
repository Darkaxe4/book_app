import csv
from drf_yasg.utils import swagger_auto_schema
from functools import lru_cache
from io import StringIO
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response


from .models import Book
from .serializers import BookSerializer

@lru_cache(maxsize=16)
def idempotent_create(**kwargs):
    return Book.objects.get_or_create(**kwargs)

class BookCreateView(APIView):
    @swagger_auto_schema(request_body=BookSerializer)
    def post(self, request):
        serializer = BookSerializer(data=request.data)
        if serializer.is_valid():
            book = idempotent_create(**serializer.data)
            return Response(book, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class BookRetrieveView(APIView):
    @swagger_auto_schema(responses={200: BookSerializer})
    def get(self, request, pk):
        try:
            book = Book.objects.get(pk=pk)
            return Response(BookSerializer(book).data)
        except Book.DoesNotExist:
            return Response({'detail': 'Book not found.'}, status=status.HTTP_404_NOT_FOUND)


class BookListView(APIView):
    @swagger_auto_schema(responses={200: BookSerializer(many=True)})
    def get(self, request):
        books = Book.objects.all()
        serializer = BookSerializer(books, many=True)
        csv_output = StringIO()
        writer = csv.writer(csv_output)
        writer.writerow(['Title', 'Page Count', 'ISBN'])
        for book in books:
            writer.writerow([book.title, book.page_count, book.isbn])

        response = Response(csv_output.getvalue(), content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="books.csv"'
        return response


class BookUpdateView(APIView):
    @swagger_auto_schema(request_body=BookSerializer, responses={200: BookSerializer})
    def put(self, request, pk):
        try:
            book = Book.objects.get(pk=pk)
            serializer = BookSerializer(book, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Book.DoesNotExist:
            return Response({'detail': 'Book not found.'}, status=status.HTTP_404_NOT_FOUND)


class BookDeleteView(APIView):
    @swagger_auto_schema(responses={204: 'No Content'})
    def delete(self, request, pk):
        try:
            book = Book.objects.get(pk=pk)
            book.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Book.DoesNotExist:
            return Response({'detail': 'Book not found.'}, status=status.HTTP_404_NOT_FOUND)
