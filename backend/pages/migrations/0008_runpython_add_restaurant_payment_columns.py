# Migration to safely add payment columns using RunPython with raw SQL

from django.db import migrations


def add_payment_columns(apps, schema_editor):
    """Add payment columns to RestaurantReservation table if they don't exist"""
    from django.db import connection
    
    with connection.cursor() as cursor:
        # Check which columns exist
        cursor.execute("""
            SELECT column_name 
            FROM information_schema.columns 
            WHERE table_name = 'pages_restaurantreservation'
        """)
        existing_columns = {row[0] for row in cursor.fetchall()}
        
        # Add price_per_person if it doesn't exist
        if 'price_per_person' not in existing_columns:
            cursor.execute("""
                ALTER TABLE pages_restaurantreservation 
                ADD COLUMN price_per_person DECIMAL(10, 2) DEFAULT 2500
            """)
            print("✓ Added price_per_person column")
        
        # Add total_amount if it doesn't exist
        if 'total_amount' not in existing_columns:
            cursor.execute("""
                ALTER TABLE pages_restaurantreservation 
                ADD COLUMN total_amount DECIMAL(10, 2) DEFAULT 0
            """)
            print("✓ Added total_amount column")
        
        # Add amount_paid if it doesn't exist
        if 'amount_paid' not in existing_columns:
            cursor.execute("""
                ALTER TABLE pages_restaurantreservation 
                ADD COLUMN amount_paid DECIMAL(10, 2) DEFAULT 0
            """)
            print("✓ Added amount_paid column")
        
        # Add payment_status if it doesn't exist
        if 'payment_status' not in existing_columns:
            cursor.execute("""
                ALTER TABLE pages_restaurantreservation 
                ADD COLUMN payment_status VARCHAR(20) DEFAULT 'pending'
            """)
            print("✓ Added payment_status column")


def reverse_columns(apps, schema_editor):
    """Reverse migration - drop columns if needed"""
    pass


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0007_add_restaurant_payment_fields_final'),
    ]

    operations = [
        migrations.RunPython(add_payment_columns, reverse_columns),
    ]
