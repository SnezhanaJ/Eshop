# Generated by Django 4.2.2 on 2023-06-19 21:45

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=255, null=True)),
                ('price', models.FloatField(blank=True, null=True)),
                ('quantity', models.IntegerField(blank=True, null=True)),
                ('code', models.CharField(blank=True, max_length=255, null=True)),
                ('category', models.CharField(choices=[('L', 'Laptop'), ('P', 'Phone'), ('TV', 'TV')], max_length=2)),
                ('image', models.ImageField(null=True, upload_to='images/')),
                ('screen', models.CharField(blank=True, max_length=255, null=True)),
                ('screenSize', models.CharField(blank=True, max_length=255, null=True)),
                ('OS', models.CharField(blank=True, max_length=255, null=True)),
                ('memory', models.CharField(blank=True, max_length=255, null=True)),
                ('CPU', models.CharField(blank=True, max_length=255, null=True)),
                ('camera', models.CharField(blank=True, max_length=255, null=True)),
                ('battery', models.CharField(blank=True, max_length=255, null=True)),
                ('RAM', models.CharField(blank=True, max_length=255, null=True)),
            ],
        ),
    ]