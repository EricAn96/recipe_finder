# Generated by Django 3.2.3 on 2021-06-06 22:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ingredients', '0004_ingredient_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ingredient',
            name='name',
            field=models.CharField(max_length=20, verbose_name='Add Ingredient'),
        ),
    ]
