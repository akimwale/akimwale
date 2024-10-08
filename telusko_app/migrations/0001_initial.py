# Generated by Django 5.0.6 on 2024-07-07 09:36

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='PLANS',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('img', models.ImageField(upload_to='pics')),
                ('price', models.IntegerField(max_length=200)),
                ('options', models.BooleanField(default=False)),
            ],
        ),
    ]
