# Generated by Django 3.2.5 on 2021-09-07 14:25

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0016_alter_orderitem_quantity'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shippingaddress',
            name='date_added',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
