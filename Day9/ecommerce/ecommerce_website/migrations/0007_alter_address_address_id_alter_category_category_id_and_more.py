# Generated by Django 5.2.2 on 2025-06-17 12:22

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ecommerce_website',
         '0006_alter_address_address_id_alter_category_category_id_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='address',
            name='address_id',
            field=models.UUIDField(default=uuid.UUID('21f66151-fe99-4fe5-8abe-5163888615b7'), editable=False, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='category',
            name='category_id',
            field=models.UUIDField(default=uuid.UUID('d72764d2-f589-4b08-850d-21e37fe5f69d'), editable=False, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='customer',
            name='customer_id',
            field=models.UUIDField(default=uuid.UUID('35be8d35-fd70-4c37-9001-002f82f2f4f7'), editable=False, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='order',
            name='order_id',
            field=models.UUIDField(default=uuid.UUID('dfcbd8f6-e9ae-493e-adb5-7229a04afada'), editable=False, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='orderitem',
            name='order_item_id',
            field=models.UUIDField(default=uuid.UUID('b71fbf51-a762-419d-8c60-dd39443e4aa4'), editable=False, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='paymentmethod',
            name='payment_methods_id',
            field=models.UUIDField(default=uuid.UUID('5672d2a0-d1aa-42ea-be9f-58ed5b194593'), editable=False, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='product',
            name='product_id',
            field=models.UUIDField(default=uuid.UUID('e4ebc19a-9b25-4a72-a819-12ea5308017d'), editable=False, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='productimage',
            name='product_image_id',
            field=models.UUIDField(default=uuid.UUID('543c9570-c138-4904-88eb-b9722afc32bd'), editable=False, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='review',
            name='review_id',
            field=models.UUIDField(default=uuid.UUID('ff8a1e10-7a4b-4e2b-af77-ad6312e5ccae'), editable=False, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='reviewimage',
            name='review_images_id',
            field=models.UUIDField(default=uuid.UUID('1fc64006-26ad-4e8b-8e0d-823b1f3f4cba'), editable=False, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='vendor',
            name='vendor_id',
            field=models.UUIDField(default=uuid.UUID('c121cac1-7e9b-4549-905c-1aaec99d615f'), editable=False, primary_key=True, serialize=False),
        ),
    ]
