# Generated by Django 5.1.1 on 2024-09-30 19:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0005_alter_category_description_alter_product_description_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='version',
            name='version_number',
            field=models.CharField(max_length=50),
        ),
    ]
