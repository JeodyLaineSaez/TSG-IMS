# Generated by Django 5.2.3 on 2025-06-30 06:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0009_rename_office_name_computer_entity_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='mr',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
