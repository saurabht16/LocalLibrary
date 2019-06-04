from django.contrib import admin

from catalog.models import Author, Genre,Book, BookInstance, Language


#admin.site.register(Author)
admin.site.register(Genre)
admin.site.register(Language)

class AuthorAdmin(admin.ModelAdmin):
   list_display =  ('last_name', 'first_name', 'date_of_birth',)


class BookInstanceInline(admin.StackedInline):
    model = BookInstance


class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'display_genre', 'language')
    inlines = [BookInstanceInline,]


class BookInstanceAdmin(admin.ModelAdmin):
    list_display = ('book', 'status', 'borrower', 'due_back', 'id')
    list_filter = ('status', 'due_back')

    fieldsets = (
        (None, {
            'fields': ('book', 'imprint', 'id')
        }),
        ('Availability', {
            'fields': ('status', 'due_back', 'borrower')
        }),
    )

admin.site.register(Author,  AuthorAdmin)
admin.site.register(Book, BookAdmin)
admin.site.register(BookInstance, BookInstanceAdmin)