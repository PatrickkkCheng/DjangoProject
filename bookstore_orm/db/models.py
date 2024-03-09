from django.db.models import Count,Max,Sum, Avg, Max, Min
from django.db.models import F
from django.db.models import Q
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.contrib.auth.models import BaseUserManager



# books = Book.objects.filter(
#     Q(author__name="J.K. Rowling") | Q(genre__name="Fantasy")
# )
# books = Book.objects.filter(
#     ~Q(genre__name="fantasy") & Q(pages__gt=300)
# )
# Book.objects.update(pages=F("pages") * 1.1)
# genre_avg = Book.objects.annotate(
#     genre_avg_price=Avg("philosophy__book__price")
# )
# # Then, filter books where the price is more than 50% higher than the genre's average
# expensive_books = genre_avg.filter(price__gt=F("genre_avg_price") * 1.5

# author_book_count = Author.objects.annotate(num_books=Count("books"))
# latest_book_per_author = Author.objects.annotate(latest_publication=Max("books__publication_date"))
# total_pages_fantasy = Book.objects.filter(genre__name="fantasy").aggregate(Sum("pages"))

# Author.objects.filter(pk__in=[1, 4, 7])
# Book.objects.filter(title__contains/icontains="House")
# Author.objects.filter(pen_name__iexact="george orwell")
# Author.objects.filter(first_name__startswith/istartswith/endswith="J")
# Book.objects.filter(pk__range=(1, 5))
# Book.objects.filter(pub_date__year=2023)
# Author.objects.filter(pk__lt/gt, gte, lt, lte=10)

###### Counts how many books each author published per year.
# books_per_year = Author.objects.annotate(year=F("book__publication_date__year")).values("year").annotate(count=Count("book"))
##### Finds the most recently published book for each genre.
# latest_book_per_genre = Genre.objects.annotate(latest_book=Max("book__publication_date"))
##### Counts the number of fantasy books written by each author.
# author_genre_count = Author.objects.filter(book__genre__name="Fantasy").annotate(fantasy_books_count=Count("book"))

# books = Book.objects.select_related("genre").all()
# for book in books:
#     print(book.title, book.genre.format)

# authors = Author.objects.prefetch_related("book_set").all()
# for author in authors:
#     for book in author.book_set.all():
#         print(book.title)

# Custom Manager for the new User model
class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("The Email field must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self.create_user(email, password, **extra_fields)

class Author(AbstractUser):
    email = models.EmailField(unique=True)
    pen_name = models.CharField(max_length=100, blank=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email

# class Author(models.Model):
#     first_name = models.CharField(max_length=100)
#     last_name = models.CharField(max_length=100)
#     pen_name = models.CharField(max_length=100, blank=True)
#
#     def __str__(self):
#         if self.pen_name:
#             return f"Author {self.pk}: {self.pen_name}"
#         else:
#             return f"Author {self.pk}: {self.first_name} {self.last_name}"

# class Badge(models.Model):
#     author = models.OneToOneField(Author, on_delete=models.CASCADE, related_name="badge")
#     badge_number = models.CharField(max_length=50)
#     issue_date = models.DateField()
#
#     def __str__(self):
#         return f"Badge for {self.author}"

class Genre(models.Model):
    format = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return f"Literary genre {self.pk}: {self.format}"


class Book(models.Model):
    COVER_CHOICES = [
        ("H", "Hard"),
        ("S", "Soft")
    ]
    title = models.CharField(max_length=100, unique=True)
    price = models.DecimalField(max_digits=5, decimal_places=2)
    cover = models.CharField(max_length=1, choices=COVER_CHOICES)
    # genre = models.ForeignKey(Genre, on_delete=models.CASCADE)
    authors = models.ManyToManyField(Author)

    def __str__(self):
        return f"Book {self.pk}: {self.title}"
