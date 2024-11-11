from django.db import models

class Admin(models.Model):
    AdminID = models.AutoField(primary_key=True)
    Username = models.CharField(max_length=50, unique=True)
    Password = models.CharField(max_length=255)

class Member(models.Model):
    MemberID = models.AutoField(primary_key=True)
    FullName = models.CharField(max_length=100)
    Email = models.EmailField(max_length=100, unique=True)
    Phone = models.CharField(max_length=15, blank=True, null=True)
    Address = models.CharField(max_length=255, blank=True, null=True)

class Publisher(models.Model):
    PublisherID = models.AutoField(primary_key=True)
    PublisherName = models.CharField(max_length=100)
    Address = models.CharField(max_length=255, blank=True, null=True)
    ContactNumber = models.CharField(max_length=15, blank=True, null=True)

class Author(models.Model):
    AuthorID = models.AutoField(primary_key=True)
    AuthorName = models.CharField(max_length=100)
    Nationality = models.CharField(max_length=50, blank=True, null=True)
    DateOfBirth = models.DateField(blank=True, null=True)

class Genre(models.Model):
    GenreID = models.AutoField(primary_key=True)
    GenreName = models.CharField(max_length=50)
    Description = models.CharField(max_length=255, blank=True, null=True)
    SubGenre = models.CharField(max_length=50, blank=True, null=True)

class Book(models.Model):
    BookID = models.AutoField(primary_key=True)
    Title = models.CharField(max_length=255)
    Author = models.ForeignKey(Author, on_delete=models.CASCADE)
    Genre = models.ForeignKey(Genre, on_delete=models.CASCADE)
    Publisher = models.ForeignKey(Publisher, on_delete=models.CASCADE)
    YearPublished = models.IntegerField()
    ISBN = models.CharField(max_length=20, unique=True)
    TotalCopies = models.IntegerField()
    AvailableCopies = models.IntegerField()

class Loan(models.Model):
    LoanID = models.AutoField(primary_key=True)
    Book = models.ForeignKey(Book, on_delete=models.CASCADE)
    Member = models.ForeignKey(Member, on_delete=models.CASCADE)
    LoanDate = models.DateField()
    ReturnDate = models.DateField(blank=True, null=True)
    DueDate = models.DateField()
    Status = models.CharField(max_length=10, choices=[('returned', 'returned'), ('overdue', 'overdue')])

class Fine(models.Model):
    FineID = models.AutoField(primary_key=True)
    Loan = models.ForeignKey(Loan, on_delete=models.CASCADE)
    FineAmount = models.DecimalField(max_digits=10, decimal_places=2)
    PaidStatus = models.CharField(max_length=10, choices=[('paid', 'paid'), ('unpaid', 'unpaid')])

class Reservation(models.Model):
    ReservationID = models.AutoField(primary_key=True)
    Book = models.ForeignKey(Book, on_delete=models.CASCADE)
    Member = models.ForeignKey(Member, on_delete=models.CASCADE)
    ReservationDate = models.DateField()
    Status = models.CharField(max_length=10, choices=[('active', 'active'), ('fulfilled', 'fulfilled')])
