# Mobile Money Transaction Analysis System

A full-stack application for analyzing Mobile Money transactions from SMS data. This system processes XML-formatted SMS messages, stores them in a database, and provides an interactive dashboard for data visualization and analysis.

## Table of Contents
- [Features](#features)
- [Project Structure](#project-structure)
- [System Architecture](#system-architecture)
- [Technical Details](#technical-details)
- [Installation & Usage](#installation--usage)

##  Features

### Core Functionality
- XML data processing and categorization
- SQLite database for transaction storage
- Interactive web dashboard with:
  - Transaction type distribution charts
  - Amount analysis by transaction type
  - Individual transaction history
  - Person-specific transaction analysis
  - Transaction type filtering
  - Dark/Light mode support
- Responsive design for all devices

## 🔧 Project Structure

```
MOMO Data-Analysis-Final/
├── app.py                 # Main Flask application
├── process_xml.py        # XML data processing and database population
├── database.py           # Database operations and queries
├── schema.sql            # Database schema and structure
├── report.pdf            # Detailed project documentation and analysis
├── static/              # Static files
│   ├── style.css        # Styling
│        
└── templates/           # HTML templates
    └── index.html       # Main template
```

##  System Architecture

### High-Level Architecture
```
┌─────────────────────────────────────────────────────────────┐
│                      Client Layer                           │
│  ┌─────────────┐    ┌─────────────┐    ┌─────────────┐     │
│  │   Browser   │    │  JavaScript │    │    CSS      │     │
│  │  Interface  │◀───│  (Charts)   │◀───│  Styling    │     │
│  └─────────────┘    └─────────────┘    └─────────────┘     │
└───────────────────────────────┬─────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────┐
│                      Application Layer                       │
│  ┌─────────────┐    ┌─────────────┐    ┌─────────────┐     │
│  │   Flask     │    │  Templates  │    │   Routes    │     │
│  │  Server     │───▶│ (Jinja2)    │◀───│  (app.py)   │     │
│  └─────────────┘    └─────────────┘    └─────────────┘     │
└───────────────────────────────┬─────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────┐
│                      Data Layer                             │
│  ┌─────────────┐    ┌─────────────┐    ┌─────────────┐     │
│  │  XML Parser │    │  Database   │    │  Data       │     │
│  │(process_xml)│───▶│ Operations  │◀───│  Models     │     │
│  └─────────────┘    └─────────────┘    └─────────────┘     │
└─────────────────────────────────────────────────────────────┘
```

### Data Flow Diagram
```
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│                 │     │                 │     │                 │
│  XML SMS Data   │────▶│  Data Processing│────▶│  SQLite Database│
│  (Input File)   │     │  (process_xml.py)│     │  (momo.db)      │
│                 │     │                 │     │                 │
└─────────────────┘     └─────────────────┘     └────────┬────────┘
                                                         │
                                                         ▼
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│                 │     │                 │     │                 │
│  Web Browser    │◀────│  Flask Server   │◀────│  Database       │
│  (Frontend)     │     │  (app.py)       │     │  Operations     │
│                 │     │                 │     │  (database.py)  │
└─────────────────┘     └─────────────────┘     └─────────────────┘
```

## 🔍 Technical Details

### Database Schema

The SQLite database uses a single table 'transactions' with the following structure:

```sql
CREATE TABLE transactions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,           -- Sender/recipient name
    amount REAL,         -- Transaction amount
    type TEXT,          -- Transaction type
    date TEXT,          -- Transaction date
    phone_number TEXT,   -- Associated phone number
    balance_after REAL   -- Balance after transaction
)
```

A complete database schema is provided in `schema.sql`, which includes:
- Detailed table structures with all necessary fields
- Indexes for optimized query performance
- Views for common analytical queries
- Transaction type definitions
- Triggers for data integrity

### Transaction Types
- Incoming Money: Money received from other users
- Payment: Payments to code holders
- Transfer: Transfers to mobile numbers
- Bank Deposit: Money deposited from bank
- Withdrawal: Cash withdrawals from agents

##  Technologies Used

### Backend
- Python 3.8+
- Flask (Web Framework)
- SQLite3 (Database)
- XML Processing (Data Extraction)

### Frontend
- HTML5/CSS3
- JavaScript
- Chart.js (Visualizations)

## 📥 Installation & Usage

1. **Prerequisites**
   - Python 3.8+
   - pip
   - Modern web browser

2. **Installation**
```bash
cd MOMO-Data-Analysis-Final
  
pip install -r requirements.txt
```

3. **Running the Application**
```bash
# First, process the XML data to populate the database
python process_xml.py

# Then start the web application
python app.py
```
Then open `http://localhost:5000` in your browser



##  License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
