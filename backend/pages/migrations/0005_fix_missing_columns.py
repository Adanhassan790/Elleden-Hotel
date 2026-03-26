# Generated migration to fix missing database columns from form fixes
# Uses direct AddField operations for better compatibility

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0004_add_payment_to_restaurant'),
    ]

    operations = [
        # Add missing payment columns to RestaurantReservation
        migrations.AddField(
            model_name='restaurantreservation',
            name='price_per_person',
            field=models.DecimalField(decimal_places=2, default=2500, max_digits=10),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='restaurantreservation',
            name='total_amount',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='restaurantreservation',
            name='amount_paid',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='restaurantreservation',
            name='payment_status',
            field=models.CharField(
                choices=[('pending', 'Pending'), ('partial', 'Partial'), ('paid', 'Paid')],
                default='pending',
                max_length=20
            ),
            preserve_default=True,
        ),
    ]
