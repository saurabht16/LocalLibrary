from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from datetime import date


class Genre(models.Model):
    """
    Model representing book genre
    """

    name = models.CharField(max_length=200, help_text='Enter a book genre \
                            (e.g. Thriller)'
                            )

    def __str__(self):
        """
        String representation pf the Model object
        :return: name
        """
        return self.name

class Book(models.Model):
    """
    Model representing a book
    """
    title = models.CharField(max_length=200)
    author = models.ForeignKey('Author', on_delete=models.SET_NULL, null=True)
    summary = models.TextField(max_length=1000, help_text='Enter a brief summary of the book'),
    isbn = models.CharField('ISBN', max_length=13, help_text='13 character ISBN Number')
    genre = models.ManyToManyField(Genre, help_text='Select a Genre for this book')
    language = models.ForeignKey('Language', help_text='Select the language of the book', on_delete=models.SET_NULL, null=True)

    def __str__(self):
        """
         String representation of the Model object
        :return: title
        """
        return self.title
    def display_genre(self):
        """
        Create a string for the genre
        :return:
        """
        return ', '.join(genre.name for genre in self.genre.all()[:3])

    display_genre.short_description = 'Genre'

    def get_absolute_url(self):
        """
        Returns the url to access the details record of the book
        :return:
        """
        return reverse('book-detail', args=[str(self.id)])


import uuid

class BookInstance(models.Model):

    """
    Model representing a specific copy of a book
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text='Unique ID for this book')
    book = models.ForeignKey('Book', on_delete=models.SET_NULL, null=True)
    imprint = models.CharField(max_length = 200)
    due_back = models.DateField(null=True, blank = True, help_text = "Due date of returning the book")
    LOAN_STATUS = (
        ('m', 'Maintenance'),
        ('o', 'On Loan'),
        ('a', 'Available'),
        ('r', 'Reserved'),
    )
    status = models.CharField(max_length=1, choices=LOAN_STATUS, blank=True, default='m',
                              help_text='Book Availability')
    borrower = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        ordering = ['due_back']
        permissions = (("can_mark_returned", "Set book as returned"),)

    def __str__(self):
        return f'{self.id} ({self.book.title})'

    @property
    def is_overdue(self):
        if self.due_back and date.today() > self.due_back:
            return True
        return False

class Author(models.Model):
    """
    Model representing Author
    """
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    date_of_birth = models.DateField(null = True, blank= True)
    date_of_death = models.DateField('Died', null = True, blank= True)

    class Meta:
        ordering = ['last_name', 'first_name']

    def __str__(self):
        return f'{self.last_name}, {self.first_name}'

class Language(models.Model):
    """
    Model representing book language
    """

    name = models.CharField(max_length=200, help_text='Enter a book language \
                            (e.g. English)'
                            )

    def __str__(self):
        """
        String representation pf the Model object
        :return: name
        """
        return self.name

class BookReview(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.PositiveSmallIntegerField(default=5)
    comment = models.TextField(max_length=1000)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Review for {self.book.title} by {self.user.username}"

class Wishlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='wishlist')
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    date_added = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'book')

    def __str__(self):
        return f"{self.user.username} wishes {self.book.title}"

class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    message = models.CharField(max_length=255)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Notification for {self.user.username}: {self.message}"

