# Generated by Django 5.1.7 on 2025-04-04 08:58

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Assignment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('description', models.TextField()),
                ('notes', models.TextField()),
                ('business', models.CharField(max_length=500)),
                ('assigned_to', models.CharField(max_length=500)),
                ('due_date', models.DateField()),
                ('status', models.CharField(max_length=500)),
                ('uploaded_by', models.CharField(max_length=500)),
            ],
        ),
    ]
