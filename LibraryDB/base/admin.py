from django.contrib import admin
from .models import Admin, Member, Publisher, Author, Genre, Book, Loan, Fine, Reservation

admin.site.register(Admin)
admin.site.register(Member)
admin.site.register(Publisher)
admin.site.register(Author)
admin.site.register(Genre)
admin.site.register(Book)
admin.site.register(Loan)
admin.site.register(Fine)
admin.site.register(Reservation)
