# Mobile Money Transaction Analysis System

A full-stack application for analyzing Mobile Money transactions from SMS data. This system processes XML-formatted SMS messages, stores them in a database, and provides an interactive dashboard for data visualization and analysis.

## 📋 Table of Contents
- [Features](#features)
- [Project Structure](#project-structure)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Running the Application](#running-the-application)
- [Usage Guide](#usage-guide)
- [Technical Details](#technical-details)
- [Development](#development)
- [Contributing](#contributing)
- [License](#license)
- [Acknowledgments](#acknowledgments)
- [System Architecture](#system-architecture)

## ✨ Features

### Core Functionality
- XML data processing and categorization
- SQLite database for transaction storage
- Interactive web dashboard with:
  - Transaction type distribution charts
  - Amount analysis by transaction type
  - Individual transaction history
  - Person-specific transaction analysis
  - Dark/Light mode support
- Responsive design for all devices

### Advanced Features
- Real-time data visualization
- Interactive transaction filtering
- Persistent theme preferences
- Detailed transaction analytics
- Mobile-responsive interface

## 🔄 System Architecture

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

### Component Interaction
```
┌─────────────────────────────────────────────────────────────┐
│                      User Interface                         │
│  ┌─────────────┐    ┌─────────────┐    ┌─────────────┐     │
│  │ Transaction │    │  Charts &   │    │  Theme      │     │
│  │   Table     │    │Visualizations│    │  Toggle     │     │
│  └─────────────┘    └─────────────┘    └─────────────┘     │
└───────────────────────────────┬─────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────┐
│                      Flask Application                       │
│  ┌─────────────┐    ┌─────────────┐    ┌─────────────┐     │
│  │   Routes    │    │  Templates  │    │  Database   │     │
│  │  (app.py)   │───▶│ (index.html)│◀───│ Operations  │     │
│  └─────────────┘    └─────────────┘    └─────────────┘     │
└───────────────────────────────┬─────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────┐
│                      Data Processing                         │
│  ┌─────────────┐    ┌─────────────┐    ┌─────────────┐     │
│  │  XML Parser │    │ Transaction │    │  Database   │     │
│  │(process_xml)│───▶│ Categorizer │───▶│  Storage    │     │
│  └─────────────┘    └─────────────┘    └─────────────┘     │
└─────────────────────────────────────────────────────────────┘
```

### Process Flow
1. **Data Input**
   - XML SMS data is read from `modified_sms_v2.xml`
   - Each SMS is parsed for transaction details

2. **Data Processing**
   - Transactions are categorized by type
   - Amounts and balances are extracted
   - Data is validated and cleaned

3. **Data Storage**
   - Processed transactions are stored in SQLite database
   - Database operations are handled by `database.py`

4. **Web Interface**
   - Flask server serves the web application
   - Templates render the dashboard
   - JavaScript handles interactivity

5. **User Interaction**
   - Users can view transaction history
   - Interactive charts show transaction distribution
   - Theme switching for better user experience

## �� Project Structure

```
momo_analysis/
├── app.py                 # Flask web application
├── database.py           # Database operations
├── process_xml.py        # XML processing and data extraction
├── requirements.txt      # Python dependencies
├── momo.db              # SQLite database file
├── modified_sms_v2.xml  # Input XML file
├── static/
│   └── style.css        # CSS styles
└── templates/
    └── index.html       # Main dashboard template
```

## 🔧 Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- Modern web browser
- Git (for version control)

## 🚀 Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/momo_analysis.git
cd momo_analysis
```

2. Create a virtual environment (recommended but optional):
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## 🏃‍♂️ Running the Application

1. Initialize the database:
```bash
python process_xml.py
```

2. Start the Flask application:
```bash
python app.py
```

3. Open your web browser and navigate to:
```
http://localhost:5000
```

## 📖 Usage Guide

### Dashboard Overview
- View all transactions in a sortable table
- See transaction distribution by type
- Analyze total amounts by transaction type
- Filter transactions by date range
- Search for specific transactions

### Individual Analysis
- Click on any person's name to view their transaction history
- Switch between pie chart and bar graph visualizations
- View detailed transaction information
- Export transaction data for specific individuals

### Theme Switching
- Toggle between dark and light modes using the button in the top-right corner
- Theme preference is saved between sessions
- Automatic theme detection based on system preferences

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

### Transaction Types

The system categorizes transactions into the following types:
- Incoming Money: Money received from other users
- Payment: Payments to code holders
- Transfer: Transfers to mobile numbers
- Bank Deposit: Money deposited from bank
- Withdrawal: Cash withdrawals from agents

### API Endpoints

- `GET /`: Main dashboard
- `GET /person/<name>`: Get person-specific transaction data
- `GET /api/transactions`: Get all transactions
- `GET /api/stats`: Get transaction statistics

## 👥 Development Team

### Core Developers
- [Your Name] r
  - Implemented XML processing
  - Designed database schema
  - Developed web interface
  - Created visualizations
  - Implemented theme switching

### Contributors
- Elvin Cyubahiro (e.cyubahiro@alustudent.com)
  - Database optimization
  - API development
  - Data processing
  - Performance improvements

- [Team Member 3] 
  - UI/UX design
  - Chart implementations
  - Theme development
  - Responsive design

## 🛠️ Technologies Used

### Backend
- Python 3.8+
- Flask (Web Framework)
- SQLite3 (Database)
- XML Processing (Data Extraction)

### Frontend
- HTML5 (Structure)
- CSS3 (Styling)
- JavaScript (Interactivity)
- Chart.js (Visualizations)

### Development Tools
- Git (Version Control)
- VS Code/PyCharm (IDE)
- Chrome DevTools (Debugging)

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- MTN Mobile Money for the transaction data format
- Chart.js for visualization capabilities
- Flask framework for web application development
- All contributors who have helped shape this project

## 📞 Support

For support, please open an issue in the GitHub repository or contact the development team. 
