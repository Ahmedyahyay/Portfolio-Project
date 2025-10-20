#!/usr/bin/env python3
"""
Quick database schema fix to add missing username column
"""

import sqlite3
import os
import sys

def fix_database_schema():
    """Add missing username column to existing database"""
    db_path = 'backend/nutrition.db'
    
    if not os.path.exists(db_path):
        print("❌ Database file not found")
        return False
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Check if username column exists
        cursor.execute("PRAGMA table_info(user)")
        columns = cursor.fetchall()
        column_names = [col[1] for col in columns]
        
        print(f"Current user table columns: {column_names}")
        
        if 'username' not in column_names:
            print("Adding username column to user table...")
            
            # Add username column
            cursor.execute("ALTER TABLE user ADD COLUMN username VARCHAR(80)")
            
            # Update existing users with usernames based on email
            cursor.execute("SELECT id, email FROM user")
            users = cursor.fetchall()
            
            for user_id, email in users:
                username = email.split('@')[0] if email else f'user_{user_id}'
                cursor.execute("UPDATE user SET username = ? WHERE id = ?", (username, user_id))
            
            # Create unique index on username
            cursor.execute("CREATE UNIQUE INDEX IF NOT EXISTS ix_user_username ON user(username)")
            
            conn.commit()
            print("✅ Username column added successfully")
        else:
            print("✅ Username column already exists")
        
        # Verify the fix
        cursor.execute("PRAGMA table_info(user)")
        columns = cursor.fetchall()
        column_names = [col[1] for col in columns]
        print(f"Updated user table columns: {column_names}")
        
        conn.close()
        return True
        
    except Exception as e:
        print(f"❌ Failed to fix database schema: {e}")
        return False

if __name__ == '__main__':
    print("🔧 Fixing database schema...")
    if fix_database_schema():
        print("✅ Database schema fixed successfully")
        print("🔄 Please restart the Flask server")
    else:
        print("❌ Failed to fix database schema")
        sys.exit(1)
