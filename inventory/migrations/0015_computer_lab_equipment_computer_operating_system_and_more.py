# Generated by Django 5.2.4 on 2025-07-08 05:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0014_borrower'),
    ]

    operations = [
        migrations.AddField(
            model_name='computer',
            name='lab_equipment',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='computer',
            name='operating_system',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='computer',
            name='source',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]
