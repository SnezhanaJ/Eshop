# Generated by Django 4.2.2 on 2023-06-30 15:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('eshop', '0021_alter_customer_date_created'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='on_sale',
            field=models.BooleanField(blank=True, default=False, null=True),
        ),
    ]
