# Generated by Django 5.1.7 on 2025-04-11 09:51

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('assignment', '0004_alter_assignment_business_delete_business'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterField(
            model_name='assignment',
            name='assigned_to',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='assignments_assigned', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='assignment',
            name='uploaded_by',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='assignments_uploaded', to=settings.AUTH_USER_MODEL),
        ),
    ]
