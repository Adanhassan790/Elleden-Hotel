from django.apps import AppConfig
from django.db import connection


class PagesConfig(AppConfig):
    name = 'pages'
    
    def ready(self):
        """Run startup tasks when the app initializes"""
        # Use a flag to prevent multiple runs (ready() can be called multiple times)
        if hasattr(self, '_ensured_columns'):
            return
        self._ensured_columns = True
        self.ensure_restaurant_payment_columns()
    
    def ensure_restaurant_payment_columns(self):
        """
        Ensure payment columns exist in RestaurantReservation table.
        This runs on app startup to handle column creation when migrations don't run.
        """
        try:
            from django.db import transaction
            from psycopg2 import Error as PostgresError
            
            with connection.cursor() as cursor:
                # Check if table exists and get existing columns
                cursor.execute("""
                    SELECT column_name 
                    FROM information_schema.columns 
                    WHERE table_name = 'pages_restaurantreservation'
                """)
                existing_columns = {row[0] for row in cursor.fetchall()}
                
                # Add missing columns (each in its own transaction to prevent abort)
                columns_to_add = {
                    'price_per_person': "DECIMAL(10, 2) DEFAULT 2500",
                    'total_amount': "DECIMAL(10, 2) DEFAULT 0",
                    'amount_paid': "DECIMAL(10, 2) DEFAULT 0",
                    'payment_status': "VARCHAR(20) DEFAULT 'pending'"
                }
                
                for col_name, col_type in columns_to_add.items():
                    if col_name not in existing_columns:
                        try:
                            # Wrap each column creation in its own atomic block
                            with transaction.atomic():
                                with connection.cursor() as col_cursor:
                                    sql = f"ALTER TABLE pages_restaurantreservation ADD COLUMN {col_name} {col_type}"
                                    col_cursor.execute(sql)
                                    print(f"✓ Added {col_name} column to RestaurantReservation")
                        except PostgresError as e:
                            if 'already exists' in str(e):
                                print(f"✓ Column {col_name} already exists")
                            else:
                                print(f"⚠ Could not add {col_name}: {str(e)}")
                        except Exception as e:
                            print(f"⚠ Could not add {col_name}: {str(e)}")
                    else:
                        print(f"✓ Column {col_name} already exists")
        
        except Exception as e:
            # Log but don't crash - app should still work
            import traceback
            print(f"⚠ Error ensuring restaurant payment columns: {str(e)}")
            traceback.print_exc()

