#!/usr/bin/env python3
"""
Fix missing username column in existing database
"""

import sqlite3
import os
import sys
import glob

def find_database():
    """Find the nutrition database file"""
    possible_locations = [
        'backend/nutrition.db',
        'nutrition.db',
        './backend/nutrition.db',
        '../backend/nutrition.db'
    ]
    
    # Also search for any .db files
    db_files = glob.glob('**/*.db', recursive=True)
    
    print("Searching for database...")
    print(f"Current directory: {os.getcwd()}")
    print(f"Found .db files: {db_files}")
    
    for location in possible_locations:
        if os.path.exists(location):
            print(f"Found database at: {location}")
            return location
    
    # Check if any .db files contain 'nutrition' or have user table
    for db_file in db_files:
        if 'nutrition' in db_file.lower():
            print(f"Found nutrition database: {db_file}")
            return db_file
        
        # Check if this db has a user table
        try:
            conn = sqlite3.connect(db_file)
            cursor = conn.cursor()
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='user'")
            if cursor.fetchone():
                print(f"Found database with user table: {db_file}")
                conn.close()
                return db_file
            conn.close()
        except:
            continue
    
    return None

def fix_username_column():
    """Add missing username column to user table"""
    db_path = find_database()
    
    if not db_path:
        print("❌ No database file found")
        print("Please make sure you're in the correct directory and the database exists")
        return False
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Check if user table exists
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='user'")
        if not cursor.fetchone():
            print("❌ No 'user' table found in database")
            return False
        
        # Check current table structure
        cursor.execute("PRAGMA table_info(user)")
        columns = cursor.fetchall()
        column_names = [col[1] for col in columns]
        
        print(f"Database: {db_path}")
        print(f"Current user table columns: {column_names}")
        
        if 'username' not in column_names:
            print("Adding username column...")
            
            # Add username column
            cursor.execute("ALTER TABLE user ADD COLUMN username VARCHAR(80)")
            
            # Get existing users and create usernames
            cursor.execute("SELECT id, email FROM user")
            users = cursor.fetchall()
            
            if users:
                print(f"Found {len(users)} existing users")
                for user_id, email in users:
                    if email:
                        username = email.split('@')[0]
                    else:
                        username = f'user_{user_id}'
                    
                    cursor.execute("UPDATE user SET username = ? WHERE id = ?", (username, user_id))
                    print(f"Set username '{username}' for user {user_id}")
            else:
                print("No existing users found")
            
            # Create unique index on username
            try:
                cursor.execute("CREATE UNIQUE INDEX ix_user_username ON user(username)")
                print("Created unique index on username")
            except sqlite3.Error as e:
                print(f"Index creation warning: {e}")
            
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
        print(f"❌ Failed to fix username column: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    print("🔧 Fixing missing username column...")
    if fix_username_column():
        print("✅ Database fixed successfully")
        print("🔄 Please restart your Flask server")
    else:
        print("❌ Failed to fix database")
        sys.exit(1)
