#!/usr/bin/env python
"""
Simple script to test PostgreSQL connection
"""
import psycopg2
import sys

def test_connection():
    print("Testing PostgreSQL connection...")
    
    try:
        # Connection parameters
        conn_params = {
            'dbname': 'test_db_1gkb',
            'user': 'test_db_1gkb_user',
            'password': 'QGeIXVtCWntGCgz463NxSbfRk70Y7hXW',
            'host': 'dpg-cu0r14l2ng1s73e22fbg-a.oregon-postgres.render.com',
            'port': '5432',
            'sslmode': 'require'
        }
        
        # Connect to the database
        conn = psycopg2.connect(**conn_params)
        
        # Create a cursor
        cur = conn.cursor()
        
        # Execute a simple query
        cur.execute('SELECT version();')
        
        # Fetch the result
        version = cur.fetchone()
        
        # Close cursor and connection
        cur.close()
        conn.close()
        
        print("Connection successful!")
        print(f"PostgreSQL version: {version[0]}")
        return True
        
    except Exception as e:
        print(f"Error connecting to PostgreSQL: {e}")
        return False

if __name__ == "__main__":
    success = test_connection()
    sys.exit(0 if success else 1) 