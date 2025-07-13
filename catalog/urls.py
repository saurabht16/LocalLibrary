from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name = 'index'),
    path('books/', views.BookListView.as_view(), name = 'books'),
    path('book/<int:pk>', views.BookDetailView.as_view(), name = 'book-detail'),
    path('mybooks/', views.LoanedBooksByUserListView.as_view(), name='my-borrowed'),
    path('book/<uuid:pk>/renew/', views.renew_book_librarian, name='renew-book-librarian'),
    path('search/', views.book_search, name='book-search'),
    path('profile/', views.user_profile, name='user-profile'),
    path('book/<int:pk>/reviews/', views.book_reviews, name='book-reviews'),
    path('book/<int:pk>/add-review/', views.add_book_review, name='add-book-review'),
    path('bookinstance/<uuid:pk>/loan/', views.loan_book, name='loan-book'),
    path('bookinstance/<uuid:pk>/return/', views.return_book, name='return-book'),
    path('wishlist/', views.wishlist, name='wishlist'),
    path('book/<int:pk>/add-to-wishlist/', views.add_to_wishlist, name='add-to-wishlist'),
    path('book/<int:pk>/remove-from-wishlist/', views.remove_from_wishlist, name='remove-from-wishlist'),
    path('notifications/', views.notifications, name='notifications'),
]