# Generated by Django 5.1.3 on 2024-11-11 09:07

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Admin',
            fields=[
                ('AdminID', models.AutoField(primary_key=True, serialize=False)),
                ('Username', models.CharField(max_length=50, unique=True)),
                ('Password', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Author',
            fields=[
                ('AuthorID', models.AutoField(primary_key=True, serialize=False)),
                ('AuthorName', models.CharField(max_length=100)),
                ('Nationality', models.CharField(blank=True, max_length=50, null=True)),
                ('DateOfBirth', models.DateField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Genre',
            fields=[
                ('GenreID', models.AutoField(primary_key=True, serialize=False)),
                ('GenreName', models.CharField(max_length=50)),
                ('Description', models.CharField(blank=True, max_length=255, null=True)),
                ('SubGenre', models.CharField(blank=True, max_length=50, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Member',
            fields=[
                ('MemberID', models.AutoField(primary_key=True, serialize=False)),
                ('FullName', models.CharField(max_length=100)),
                ('Email', models.EmailField(max_length=100, unique=True)),
                ('Phone', models.CharField(blank=True, max_length=15, null=True)),
                ('Address', models.CharField(blank=True, max_length=255, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Publisher',
            fields=[
                ('PublisherID', models.AutoField(primary_key=True, serialize=False)),
                ('PublisherName', models.CharField(max_length=100)),
                ('Address', models.CharField(blank=True, max_length=255, null=True)),
                ('ContactNumber', models.CharField(blank=True, max_length=15, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Book',
            fields=[
                ('BookID', models.AutoField(primary_key=True, serialize=False)),
                ('Title', models.CharField(max_length=255)),
                ('YearPublished', models.IntegerField()),
                ('ISBN', models.CharField(max_length=20, unique=True)),
                ('TotalCopies', models.IntegerField()),
                ('AvailableCopies', models.IntegerField()),
                ('Author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='base.author')),
                ('Genre', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='base.genre')),
                ('Publisher', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='base.publisher')),
            ],
        ),
        migrations.CreateModel(
            name='Loan',
            fields=[
                ('LoanID', models.AutoField(primary_key=True, serialize=False)),
                ('LoanDate', models.DateField()),
                ('ReturnDate', models.DateField(blank=True, null=True)),
                ('DueDate', models.DateField()),
                ('Status', models.CharField(choices=[('returned', 'returned'), ('overdue', 'overdue')], max_length=10)),
                ('Book', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='base.book')),
                ('Member', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='base.member')),
            ],
        ),
        migrations.CreateModel(
            name='Fine',
            fields=[
                ('FineID', models.AutoField(primary_key=True, serialize=False)),
                ('FineAmount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('PaidStatus', models.CharField(choices=[('paid', 'paid'), ('unpaid', 'unpaid')], max_length=10)),
                ('Loan', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='base.loan')),
            ],
        ),
        migrations.CreateModel(
            name='Reservation',
            fields=[
                ('ReservationID', models.AutoField(primary_key=True, serialize=False)),
                ('ReservationDate', models.DateField()),
                ('Status', models.CharField(choices=[('active', 'active'), ('fulfilled', 'fulfilled')], max_length=10)),
                ('Book', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='base.book')),
                ('Member', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='base.member')),
            ],
        ),
    ]