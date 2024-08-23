# Generated by Django 5.0.6 on 2024-08-04 15:19

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_payment_remove_invoice_payment_method_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='invoice',
            name='payment_status',
        ),
        migrations.AddField(
            model_name='invoice',
            name='payment_method',
            field=models.CharField(choices=[('gift_card', 'Gift Card'), ('crypto', 'Cryptocurrency'), ('manual', 'Manual Payment (Email/Telegram)')], default=1, max_length=50),
        ),
        migrations.AddField(
            model_name='invoice',
            name='status',
            field=models.CharField(default='Pending', max_length=20),
        ),
        migrations.AlterField(
            model_name='invoice',
            name='key_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.keytype'),
        ),
    ]
