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
from database import get_all_transactions, get_transaction_stats, get_person_transactions
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
                         chart_labels=json.dumps(chart_labels),
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

if __name__ == '__main__':
    app.run(debug=True)