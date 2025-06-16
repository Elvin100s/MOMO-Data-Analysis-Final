"""
Database Management Module for Mobile Money Transactions

This module handles all database operations for the Mobile Money transaction system.
It provides functions for creating the database, inserting transactions, and retrieving data.

The database uses SQLite and includes a single table 'transactions' with the following schema:
- id: INTEGER PRIMARY KEY AUTOINCREMENT
- name: TEXT (sender/recipient name)
- amount: REAL (transaction amount)
- type: TEXT (transaction type)
- date: TEXT (transaction date)
- phone_number: TEXT (associated phone number)
- balance_after: REAL (balance after transaction)
"""

import sqlite3
from datetime import datetime

def create_database():
    """
    Create the SQLite database and transactions table if they don't exist.
    
    The function:
    1. Connects to SQLite database (creates if not exists)
    2. Creates transactions table with required fields
    3. Sets up appropriate data types and constraints
    """
    conn = sqlite3.connect('momo.db')
    cursor = conn.cursor()
    
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS transactions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        amount REAL,
        type TEXT,
        date TEXT,
        phone_number TEXT,
        balance_after REAL
    )
    ''')
    
    conn.commit()
    conn.close()

def insert_transaction(name, amount, trans_type, date, phone_number, balance_after):
    """
    Insert a new transaction record into the database.
    
    Args:
        name (str): Name of sender/recipient
        amount (float): Transaction amount
        trans_type (str): Type of transaction
        date (str): Transaction date
        phone_number (str): Associated phone number
        balance_after (float): Balance after transaction
    """
    conn = sqlite3.connect('momo.db')
    cursor = conn.cursor()
    
    cursor.execute('''
    INSERT INTO transactions (name, amount, type, date, phone_number, balance_after)
    VALUES (?, ?, ?, ?, ?, ?)
    ''', (name, amount, trans_type, date, phone_number, balance_after))
    
    conn.commit()
    conn.close()

def get_all_transactions():
    """
    Retrieve all transactions from the database.
    
    Returns:
        list: List of tuples containing all transaction records,
              ordered by date in descending order
    """
    conn = sqlite3.connect('momo.db')
    cursor = conn.cursor()
    
    cursor.execute('SELECT * FROM transactions ORDER BY date DESC')
    transactions = cursor.fetchall()
    
    conn.close()
    return transactions

def get_transaction_stats():
    """
    Get statistical information about transactions.
    
    Returns:
        list: List of tuples containing:
              - Transaction type
              - Count of transactions
              - Total amount for each type
    """
    conn = sqlite3.connect('momo.db')
    cursor = conn.cursor()
    
    cursor.execute('''
    SELECT type, COUNT(*) as count, SUM(amount) as total 
    FROM transactions 
    GROUP BY type
    ''')
    stats = cursor.fetchall()
    
    conn.close()
    return stats

def get_person_transactions(name):
    """
    Retrieve all transactions for a specific person.
    
    Args:
        name (str): Name of the person to search for
        
    Returns:
        list: List of tuples containing all transactions for the specified person,
              ordered by date in descending order
    """
    conn = sqlite3.connect('momo.db')
    cursor = conn.cursor()
    
    cursor.execute('''
    SELECT * FROM transactions 
    WHERE name = ? 
    ORDER BY date DESC
    ''', (name,))
    
    transactions = cursor.fetchall()
    conn.close()
    return transactions

def get_transactions_by_type(trans_type):
    """
    Retrieve all transactions of a specific type.
    
    Args:
        trans_type (str): Type of transaction to search for
        
    Returns:
        list: List of tuples containing all transactions of the specified type,
              ordered by date in descending order
    """
    conn = sqlite3.connect('momo.db')
    cursor = conn.cursor()
    
    cursor.execute('''
    SELECT * FROM transactions 
    WHERE type = ? 
    ORDER BY date DESC
    ''', (trans_type,))
    
    transactions = cursor.fetchall()
    conn.close()
    return transactions