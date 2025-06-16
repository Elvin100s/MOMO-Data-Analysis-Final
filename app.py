"""
Flask Web Application for Mobile Money Transaction Analysis

This module implements a web interface for analyzing Mobile Money transactions.
It provides routes for viewing transaction data and generating visualizations.

Features:
- Dashboard with transaction overview
- Transaction type distribution charts
- Individual transaction history
- Person-specific transaction analysis
"""

from flask import Flask, render_template, jsonify
from database import get_all_transactions, get_transaction_stats, get_person_transactions, get_transactions_by_type
import json

app = Flask(__name__)

@app.route('/')
def dashboard():
    """
    Main dashboard route that displays the transaction overview.
    
    Returns:
        Rendered template with:
        - List of all transactions
        - Transaction type distribution data
        - Amount distribution data
    """
    transactions = get_all_transactions()
    stats = get_transaction_stats()
    
    # Prepare data for chart visualization
    chart_labels = [stat[0] for stat in stats]
    chart_counts = [stat[1] for stat in stats]
    chart_totals = [stat[2] for stat in stats]
    
    return render_template('index.html', 
                         transactions=transactions,
                         chart_labels=chart_labels,
                         chart_counts=json.dumps(chart_counts),
                         chart_totals=json.dumps(chart_totals))

@app.route('/person/<name>')
def person_transactions(name):
    """
    API endpoint for retrieving person-specific transaction data.
    
    Args:
        name (str): Name of the person to get transactions for
        
    Returns:
        JSON response containing:
        - Person's name
        - Transaction type labels
        - Transaction amounts by type
    """
    transactions = get_person_transactions(name)
    
    # Group transactions by type and calculate totals
    type_totals = {}
    for trans in transactions:
        trans_type = trans[3]  # type column
        amount = trans[2]      # amount column
        type_totals[trans_type] = type_totals.get(trans_type, 0) + amount
    
    return jsonify({
        'name': name,
        'labels': list(type_totals.keys()),
        'values': list(type_totals.values())
    })

@app.route('/transactions/<trans_type>')
def transactions_by_type(trans_type):
    """
    API endpoint for retrieving transactions of a specific type.
    
    Args:
        trans_type (str): Type of transaction to filter by
        
    Returns:
        JSON response containing:
        - Transaction type
        - List of unique people who made this type of transaction
        - Transaction details for each person
    """
    transactions = get_transactions_by_type(trans_type)
    
    # Get unique people who made this type of transaction
    people = set()
    people_transactions = {}
    
    for trans in transactions:
        name = trans[1]  # name column
        people.add(name)
        if name not in people_transactions:
            people_transactions[name] = []
        people_transactions[name].append({
            'amount': trans[2],
            'date': trans[4],
            'phone_number': trans[5],
            'balance_after': trans[6]
        })
    
    return jsonify({
        'type': trans_type,
        'people': list(people),
        'transactions': people_transactions
    })

if __name__ == '__main__':
    app.run(debug=True)