# Generated by Django 5.0 on 2023-12-21 20:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ShopAPI', '0002_remove_cartitem_price'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('Pending', 'Pending'), ('Processed', 'Processed'), ('Cancelled', 'Cancelled')], default='Pending', max_length=20),
        ),
        migrations.DeleteModel(
            name='Status',
        ),
    ]
