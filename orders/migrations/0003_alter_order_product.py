# Generated by Django 4.2.7 on 2023-12-05 15:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0004_alter_productcategory_name_alter_productimage_image_and_more'),
        ('orders', '0002_order_product'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='product',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='main_app.product'),
        ),
    ]
