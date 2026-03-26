# Generated migration to fix missing database columns from form fixes
# Uses SQL to safely add columns if they don't exist (idempotent for PostgreSQL)

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0004_add_payment_to_restaurant'),
    ]

    operations = [
        # Add missing payment columns to RestaurantReservation using raw SQL
        # Using PostgreSQL's "IF NOT EXISTS" syntax for idempotency
        migrations.RunSQL(
            sql="""
            DO $$
            BEGIN
                IF NOT EXISTS (
                    SELECT 1 FROM information_schema.columns 
                    WHERE table_name='pages_restaurantreservation' AND column_name='price_per_person'
                ) THEN
                    ALTER TABLE pages_restaurantreservation ADD COLUMN price_per_person NUMERIC(10,2) DEFAULT 2500;
                END IF;
                
                IF NOT EXISTS (
                    SELECT 1 FROM information_schema.columns 
                    WHERE table_name='pages_restaurantreservation' AND column_name='total_amount'
                ) THEN
                    ALTER TABLE pages_restaurantreservation ADD COLUMN total_amount NUMERIC(10,2) DEFAULT 0;
                END IF;
                
                IF NOT EXISTS (
                    SELECT 1 FROM information_schema.columns 
                    WHERE table_name='pages_restaurantreservation' AND column_name='amount_paid'
                ) THEN
                    ALTER TABLE pages_restaurantreservation ADD COLUMN amount_paid NUMERIC(10,2) DEFAULT 0;
                END IF;
                
                IF NOT EXISTS (
                    SELECT 1 FROM information_schema.columns 
                    WHERE table_name='pages_restaurantreservation' AND column_name='payment_status'
                ) THEN
                    ALTER TABLE pages_restaurantreservation ADD COLUMN payment_status VARCHAR(20) DEFAULT 'pending';
                END IF;
            END $$;
            """,
            reverse_sql="-- This migration cannot be safely reversed",
        ),
    ]
