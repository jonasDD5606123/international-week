# features/environment.py
from behave import *
from database import get_connection
import sqlite3
import time

def before_all(context):
    # Set higher timeout for all operations
    sqlite3.register_adapter(bool, int)
    sqlite3.register_converter("BOOLEAN", lambda v: bool(int(v)))

def before_scenario(context, scenario):
    context.db_conn = get_connection()
    context.db_conn.isolation_level = None  # Enable autocommit

def after_scenario(context, scenario):
    if hasattr(context, 'db_conn'):
        # Clean up test data
        cursor = context.db_conn.cursor()
        try:
            cursor.execute("DELETE FROM Users WHERE naam LIKE 'test%'")
            cursor.execute("DELETE FROM Reserveringen WHERE user_id IN (SELECT id FROM Users WHERE naam LIKE 'test%')")
            cursor.execute("DELETE FROM Verslagen WHERE user_id IN (SELECT id FROM Users WHERE naam LIKE 'test%')")
            context.db_conn.commit()
        finally:
            context.db_conn.close()