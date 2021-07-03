from django.db import models
from django.contrib.auth.models import User
# Create your models here.



class ObjManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_deleted=False)


class BaseModel(models.Model):
    is_deleted = models.BooleanField(default=False)
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='Created Time')
    updated_time = models.DateTimeField(auto_now=True, verbose_name='Updated Time')
    objects = ObjManager()
    original_objects = models.Manager()

    class Meta:
        abstract = True

    def delete(self):
        self.is_deleted = True
        self.save()


class Book(BaseModel):
    book_name = models.CharField(max_length=100)
    author = models.CharField(max_length=255,blank=True)
    book_count = models.PositiveIntegerField(default=0)
    
    def __str__(self):
        return self.book_name


class Borrower(BaseModel):
	user = models.ForeignKey(User, related_name='borrower_user', on_delete=models.CASCADE)
	book = models.ForeignKey(Book, related_name='borrowed_book', on_delete=models.CASCADE)
	borrow_date = models.DateTimeField(auto_now_add=True, verbose_name='Borrowed Time')