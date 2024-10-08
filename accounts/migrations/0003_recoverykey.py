# Generated by Django 5.0.6 on 2024-08-04 08:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_keytype_paymentmethod_alter_customer_profile_pic_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='RecoveryKey',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=100)),
                ('social_media_account', models.CharField(max_length=100)),
                ('last_used_password', models.CharField(blank=True, max_length=100, null=True)),
                ('id_card_upload', models.FileField(upload_to='id_cards/')),
                ('contact_info', models.EmailField(max_length=254)),
            ],
        ),
    ]
