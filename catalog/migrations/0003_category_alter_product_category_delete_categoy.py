# Generated by Django 5.1.1 on 2024-09-22 11:47

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0002_alter_categoy_options_alter_product_category'),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150, verbose_name='наименование')),
                ('description', models.CharField(max_length=150, verbose_name='описание')),
            ],
            options={
                'verbose_name': 'категория',
                'verbose_name_plural': 'категории',
            },
        ),
        migrations.AlterField(
            model_name='product',
            name='category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='catalog.category', verbose_name='категория'),
        ),
        migrations.DeleteModel(
            name='Categoy',
        ),
    ]
