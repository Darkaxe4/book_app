from django.db import models
from django.db.models import CharField, IntegerField


class Book(models.Model):
    title = CharField(max_length=255, verbose_name="Название")
    page_count = IntegerField(verbose_name="Количество страниц")
    isbn = models.CharField(max_length=13, unique=True)

    def __str__(self):
        return self.title