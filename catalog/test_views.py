import datetime
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from catalog.models import (
    Book, Author, Genre, Language, BookInstance, Wishlist
)

class TestWishlist(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(username='wishuser', password='wishpass')

        genre = Genre.objects.create(name="Mystery")
        language = Language.objects.create(name="English")
        author = Author.objects.create(first_name="Agatha", last_name="Christie")

        self.book = Book.objects.create(
            title='Test Book',
            author=author,
            summary="Detective story",
            isbn='1234567890123',
            language=language,
        )
        self.book.genre.set([genre])

        Wishlist.objects.create(user=self.user, book=self.book)
        self.client.login(username='wishuser', password='wishpass')

    def test_wishlist_list(self):
        response = self.client.get(reverse('wishlist'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Book')

class TestLoanedBooksView(TestCase):
    def setUp(self):
        # Create user and login
        self.user = get_user_model().objects.create_user(
            username='loanuser',
            password='loanpass'
        )
        self.client.login(username='loanuser', password='loanpass')

        # Create required related objects
        self.genre = Genre.objects.create(name="Fiction")
        self.language = Language.objects.create(name="English")
        self.author = Author.objects.create(first_name="John", last_name="Doe")

        # Create a book
        self.book = Book.objects.create(
            title="Loan Book",
            author=self.author,
            summary="Test Summary",
            isbn="1234567890123",
            language=self.language,
        )
        self.book.genre.set([self.genre])

        # Create a loaned book instance
        self.book_instance = BookInstance.objects.create(
            book=self.book,
            imprint="Test Imprint",
            due_back=datetime.date.today() + datetime.timedelta(days=7),
            status='o',  # On loan
            borrower=self.user
        )

    def test_loaned_book_is_listed(self):
        """Test that the user's loaned book appears in the my-borrowed view."""
        response = self.client.get(reverse('my-borrowed'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Loan Book")
        self.assertContains(response, self.book_instance.due_back.strftime('%B %d, %Y'))