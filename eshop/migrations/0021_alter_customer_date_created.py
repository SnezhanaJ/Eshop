# Generated by Django 4.2.2 on 2023-06-30 14:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('eshop', '0020_remove_customer_customer_image_remove_customer_email_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='date_created',
            field=models.DateTimeField(auto_now=True, null=True),
        ),
    ]