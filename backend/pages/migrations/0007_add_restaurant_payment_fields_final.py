# Direct SQL migration to add payment fields to RestaurantReservation

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0006_add_payment_columns_with_error_handling'),
    ]

    operations = [
        # Add all 4 payment fields in one migration
        # These operations are safe - Django will skip them if the fields already exist
        migrations.AddField(
            model_name='restaurantreservation',
            name='price_per_person',
            field=models.DecimalField(decimal_places=2, default=2500, max_digits=10),
        ),
        migrations.AddField(
            model_name='restaurantreservation',
            name='total_amount',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
        ),
        migrations.AddField(
            model_name='restaurantreservation',
            name='amount_paid',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
        ),
        migrations.AddField(
            model_name='restaurantreservation',
            name='payment_status',
            field=models.CharField(
                choices=[('pending', 'Pending'), ('partial', 'Partial'), ('paid', 'Paid')],
                default='pending',
                max_length=20
            ),
        ),
    ]
