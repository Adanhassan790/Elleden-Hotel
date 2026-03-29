# Data migration to safely add restaurant payment columns with error handling

from django.db import migrations, models


def add_columns_if_missing(apps, schema_editor):
    """Add payment columns to RestaurantReservation if they don't exist"""
    from django.db import connection
    
    with connection.cursor() as cursor:
        # Check if columns exist
        cursor.execute("""
            SELECT column_name 
            FROM information_schema.columns 
            WHERE table_name='pages_restaurantreservation' 
            AND column_name IN ('price_per_person', 'total_amount', 'amount_paid', 'payment_status')
        """)
        existing_columns = {row[0] for row in cursor.fetchall()}
        
        # Add missing columns
        if 'price_per_person' not in existing_columns:
            cursor.execute("""
                ALTER TABLE pages_restaurantreservation 
                ADD COLUMN price_per_person DECIMAL(10, 2) DEFAULT 2500 NOT NULL
            """)
        
        if 'total_amount' not in existing_columns:
            cursor.execute("""
                ALTER TABLE pages_restaurantreservation 
                ADD COLUMN total_amount DECIMAL(10, 2) DEFAULT 0 NOT NULL
            """)
        
        if 'amount_paid' not in existing_columns:
            cursor.execute("""
                ALTER TABLE pages_restaurantreservation 
                ADD COLUMN amount_paid DECIMAL(10, 2) DEFAULT 0 NOT NULL
            """)
        
        if 'payment_status' not in existing_columns:
            cursor.execute("""
                ALTER TABLE pages_restaurantreservation 
                ADD COLUMN payment_status VARCHAR(20) DEFAULT 'pending' NOT NULL
            """)


def reverse_columns(apps, schema_editor):
    """Reverse migration - drop columns if they exist"""
    from django.db import connection
    
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT column_name 
            FROM information_schema.columns 
            WHERE table_name='pages_restaurantreservation' 
            AND column_name IN ('price_per_person', 'total_amount', 'amount_paid', 'payment_status')
        """)
        existing_columns = {row[0] for row in cursor.fetchall()}
        
        # Drop existing columns
        if existing_columns:
            columns = ', '.join(existing_columns)
            cursor.execute(f"""
                ALTER TABLE pages_restaurantreservation 
                DROP COLUMN IF EXISTS {', DROP COLUMN IF EXISTS '.join(existing_columns)} CASCADE
            """)


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0005_safely_add_restaurant_payment_fields'),
    ]

    operations = [
        migrations.RunPython(add_columns_if_missing, reverse_columns),
    ]
