# Generated migration - Re-add payment fields to RestaurantReservation
# In case 0004 migration didn't apply successfully

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0004_add_payment_to_restaurant'),
    ]

    operations = [
        # These AddField operations are idempotent - they won't fail if the field already exists
        # Django will simply skip them if the field is already present in the database
        migrations.AddField(
            model_name='restaurantreservation',
            name='price_per_person',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='restaurantreservation',
            name='total_amount',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='restaurantreservation',
            name='amount_paid',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='restaurantreservation',
            name='payment_status',
            field=models.CharField(
                choices=[('pending', 'Pending'), ('partial', 'Partial'), ('paid', 'Paid')],
                default='pending',
                max_length=20
            ),
            preserve_default=False,
        ),
    ]
