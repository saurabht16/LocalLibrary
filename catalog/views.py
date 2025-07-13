from django.shortcuts import render, get_object_or_404
from django.views import generic
from catalog.models import Book, Author, BookInstance, Genre, Language, BookReview, Wishlist, Notification
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
import datetime
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import permission_required
from django.db.models import Q
from django.contrib.auth.models import User
from django.shortcuts import redirect

from catalog.forms import RenewBookForm

@login_required
def index(request):
    """
    View function for home page of the site
    """

    num_books = Book.objects.all().count()
    num_instances = BookInstance.objects.all().count()
    num_instance_available = BookInstance.objects.filter(status__exact='a').count()
    num_authors = Author.objects.all().count()
    num_visits = request.session.get('num_visits', 0)
    request.session['num_visits'] = num_visits + 1

    context = {
       'num_books' : num_books,
       'num_instances' : num_instances,
       'num_instance_available' :  num_instance_available,
       'num_authors' : num_authors,
        'num_visits' : num_visits,
    }
    return render(request, 'index.html', context = context)


class BookListView(LoginRequiredMixin, generic.ListView):
    model = Book
    paginate_by = 1


class BookDetailView(LoginRequiredMixin, generic.DetailView):
    model = Book

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        book = self.object
        context['in_wishlist'] = False
        if user.is_authenticated:
            context['in_wishlist'] = book.wishlist_set.filter(user=user).exists()
        return context


class LoanedBooksByUserListView(LoginRequiredMixin, generic.ListView):
    """Generic class-based view listing books on loan to current user."""
    model = BookInstance
    template_name = 'catalog/bookinstance_list_borrowed_user.html'
    paginate_by = 10

    def get_queryset(self):
        return BookInstance.objects.filter(borrower=self.request.user).filter(status__exact='o').order_by('due_back')


@permission_required('catalog.can_mark_returned')
def renew_book_librarian(request, pk):
    """View function for renewing a specific BookInstance by librarian."""
    book_instance = get_object_or_404(BookInstance, pk=pk)

    # If this is a POST request then process the Form data
    if request.method == 'POST':

        # Create a form instance and populate it with data from the request (binding):
        form = RenewBookForm(request.POST)

        # Check if the form is valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required (here we just write it to the model due_back field)
            book_instance.due_back = form.cleaned_data['renewal_date']
            book_instance.save()

            # redirect to a new URL:
            return HttpResponseRedirect(reverse('all-borrowed') )

    # If this is a GET (or any other method) create the default form.
    else:
        proposed_renewal_date = datetime.date.today() + datetime.timedelta(weeks=3)
        form = RenewBookForm(initial={'renewal_date': proposed_renewal_date})

    context = {
        'form': form,
        'book_instance': book_instance,
    }

    return render(request, 'catalog/book_renew_librarian.html', context)

@login_required
def book_search(request):
    query = request.GET.get('q', '')
    results = []
    if query:
        results = Book.objects.filter(
            Q(title__icontains=query) | Q(author__name__icontains=query)
        )
    context = {
        'query': query,
        'results': results,
    }
    return render(request, 'catalog/book_search.html', context)

@login_required
def user_profile(request):
    user = request.user
    reviews = BookReview.objects.filter(user=user)
    return render(request, 'catalog/user_profile.html', {'user': user, 'reviews': reviews})

@login_required
def book_reviews(request, pk):
    book = get_object_or_404(Book, pk=pk)
    reviews = book.reviews.all()
    return render(request, 'catalog/book_reviews.html', {'book': book, 'reviews': reviews})

@login_required
def add_book_review(request, pk):
    book = get_object_or_404(Book, pk=pk)
    if request.method == 'POST':
        rating = int(request.POST.get('rating', 5))
        comment = request.POST.get('comment', '')
        BookReview.objects.create(book=book, user=request.user, rating=rating, comment=comment)
        return redirect('book-reviews', pk=book.pk)
    return render(request, 'catalog/add_book_review.html', {'book': book})

@login_required
def loan_book(request, pk):
    copy = get_object_or_404(BookInstance, pk=pk)
    if copy.status == 'a':
        copy.status = 'o'
        copy.borrower = request.user
        # Set due_back to 2 weeks from today
        copy.due_back = datetime.date.today() + datetime.timedelta(weeks=2)
        copy.save()
    return HttpResponseRedirect(reverse('book-detail', args=[str(copy.book.pk)]))

@login_required
def return_book(request, pk):
    copy = get_object_or_404(BookInstance, pk=pk)
    if copy.status == 'o' and copy.borrower == request.user:
        copy.status = 'a'
        copy.borrower = None
        copy.due_back = None
        copy.save()
    return HttpResponseRedirect(reverse('book-detail', args=[str(copy.book.pk)]))

@login_required
def add_to_wishlist(request, pk):
    book = get_object_or_404(Book, pk=pk)
    Wishlist.objects.get_or_create(user=request.user, book=book)
    return redirect('book-detail', pk=pk)

@login_required
def remove_from_wishlist(request, pk):
    book = get_object_or_404(Book, pk=pk)
    Wishlist.objects.filter(user=request.user, book=book).delete()
    return redirect('book-detail', pk=pk)

@login_required
def wishlist(request):
    books = Book.objects.filter(wishlist__user=request.user)
    return render(request, 'catalog/wishlist.html', {'books': books})

@login_required
def notifications(request):
    notes = Notification.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'catalog/notifications.html', {'notifications': notes})

# Helper: Notify users when a wished book becomes available
# Call this in your loan_book and return_book views after a book is returned

def notify_wishlist_users(book):
    wished_users = User.objects.filter(wishlist__book=book)
    for user in wished_users:
        Notification.objects.create(
            user=user,
            message=f"'{book.title}' is now available!"
        )
