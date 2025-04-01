import sqlite3
import streamlit as st

# Create and return a SQLite connection
def create_connection():
    try:
        conn = sqlite3.connect("database.db", check_same_thread=False)
        return conn
    except sqlite3.Error as e:
        st.error(f"Database connection failed: {e}")
        return None

# Initialize database connection
conn = create_connection()
if conn:
    cursor = conn.cursor()

# Register a new visitor
def reg(data):
    try:
        cursor.execute('''
            INSERT INTO visitor ("Name", "Purpose", "Contact", "Date") 
            VALUES (?, ?, ?, ?)''', data)
        conn.commit()
        return True
    except sqlite3.Error as e:
        st.error(f"Something went wrong during registration: {e}")
        return False

# Login a visitor
def login(data):
    try:
        cursor.execute('''
            SELECT * FROM visitor 
            WHERE "Name" = ? AND "Contact" = ?''', data)
        return cursor.fetchone()
    except sqlite3.Error as e:
        st.error(f"Something went wrong during login: {e}")
        return None

# View all visitor records
def view():
    try:
        cursor.execute('SELECT * FROM visitor')
        return cursor.fetchall()
    except sqlite3.Error as e:
        st.error(f"Something went wrong while fetching data: {e}")
        return []

# Update a visitor record
def update(data):
    try:
        cursor.execute('''
            UPDATE visitor 
            SET "Name" = ?, "Purpose" = ?, "Contact" = ?, "Date" = ? 
            WHERE "ID" = ?''', data)
        conn.commit()
        return True
    except sqlite3.Error as e:
        st.error(f"Something went wrong during update: {e}")
        return False

# Read one visitor record by ID
def readone(id):
    try:
        cursor.execute('SELECT * FROM visitor WHERE "ID" = ?', (id,))
        return cursor.fetchone()
    except sqlite3.Error as e:
        st.error(f"Something went wrong while reading the record: {e}")
        return None

# Delete a visitor record by ID
def delete(id):
    try:
        cursor.execute('DELETE FROM visitor WHERE "ID" = ?', (id,))
        if cursor.rowcount != 0:
            conn.commit()
            return True
        else:
            st.error("No matching records found for deletion.")
            return False
    except sqlite3.Error as e:
        st.error(f"Something went wrong during deletion: {e}")
        return False
