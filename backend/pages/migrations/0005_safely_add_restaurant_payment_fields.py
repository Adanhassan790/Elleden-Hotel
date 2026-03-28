# Migration to safely add payment fields to RestaurantReservation
# Uses RunPython to handle cases where columns might already exist or partially exist

from django.db import migrations, models
from django.db.backends.postgresql.schema import DatabaseSchemaEditor


def add_columns_safely(apps, schema_editor):
    """Add payment columns to pages_restaurantreservation if they don't exist"""
    # Get the connection
    connection = schema_editor.connection
    cursor = connection.cursor()
    
    table_name = 'pages_restaurantreservation'
    columns_to_add = [
        ('price_per_person', 'NUMERIC(10, 2) DEFAULT 2500'),
        ('total_amount', 'NUMERIC(10, 2) DEFAULT 0'),
        ('amount_paid', 'NUMERIC(10, 2) DEFAULT 0'),
        ('payment_status', "VARCHAR(20) DEFAULT 'pending'"),
    ]
    
    try:
        # Check which columns already exist
        cursor.execute(f"""
            SELECT column_name FROM information_schema.columns 
            WHERE table_name = '{table_name}' AND table_schema = 'public'
        """)
        existing_columns = {row[0] for row in cursor.fetchall()}
        
        # Add missing columns
        for col_name, col_type in columns_to_add:
            if col_name not in existing_columns:
                alter_sql = f"ALTER TABLE {table_name} ADD COLUMN {col_name} {col_type}"
                cursor.execute(alter_sql)
                print(f"✓ Added column {col_name} to {table_name}")
            else:
                print(f"→ Column {col_name} already exists")
        
        # Add payment_status constraint if it doesn't exist
        cursor.execute(f"""
            SELECT constraint_name FROM information_schema.check_constraints 
            WHERE table_name = '{table_name}' AND constraint_name LIKE '%payment_status%'
        """)
        if not cursor.fetchone():
            cursor.execute(f"""
                ALTER TABLE {table_name} 
                ADD CONSTRAINT pages_restaurantreservation_payment_status_check 
                CHECK (payment_status IN ('pending', 'partial', 'paid'))
            """)
            print(f"✓ Added payment_status check constraint")
        
        connection.commit()
        print("✓ All payment columns successfully added or verified to exist")
    except Exception as e:
        connection.rollback()
        print(f"⚠ Error adding columns: {e}")
        raise


def remove_columns_safely(apps, schema_editor):
    """Reverse migration - would remove columns if needed"""
    pass


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0004_add_payment_to_restaurant'),
    ]

    operations = [
        migrations.RunPython(add_columns_safely, remove_columns_safely),
    ]
