# Generated by Django 5.0.6 on 2024-08-05 13:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0010_cryptoaddress_paymentmethodredirect_giftcardpayment'),
    ]

    operations = [
        migrations.CreateModel(
            name='CryptoWallet',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('currency', models.CharField(choices=[('bitcoin', 'Bitcoin'), ('usdt', 'USDT'), ('ethereum', 'Ethereum')], max_length=20, unique=True)),
                ('address', models.CharField(max_length=255, unique=True)),
            ],
        ),
        migrations.DeleteModel(
            name='CryptoAddress',
        ),
    ]
