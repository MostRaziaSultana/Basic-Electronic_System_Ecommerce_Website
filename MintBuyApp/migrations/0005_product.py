# Generated by Django 4.2.4 on 2023-09-12 15:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('MintBuyApp', '0004_alter_categories_slug'),
    ]

    operations = [
        migrations.CreateModel(
            name='PRODUCT',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('slug', models.SlugField(auto_created=True, unique=True)),
                ('title', models.CharField(max_length=15)),
                ('image', models.ImageField(upload_to='PROD_PIC/')),
                ('condition', models.CharField(choices=[('NEW', 'NEW'), ('OLD', 'OLD')], max_length=3)),
                ('price', models.DecimalField(decimal_places=2, max_digits=7)),
                ('description', models.TextField(max_length=250)),
            ],
        ),
    ]
