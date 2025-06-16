-- MoMo Data Analysis Database Schema
-- This schema defines the structure for storing and analyzing MTN Mobile Money transaction data

-- Enable foreign key constraints
PRAGMA foreign_keys = ON;

-- Create transactions table to store all transaction data
CREATE TABLE IF NOT EXISTS transactions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    transaction_id TEXT UNIQUE,           -- Unique transaction identifier
    name TEXT,                           -- Sender/recipient name
    amount REAL NOT NULL,                 -- Transaction amount in RWF
    type TEXT NOT NULL,                    -- Transaction type (e.g., 'Incoming Money', 'Payment', etc.)
    date DATETIME NOT NULL,               -- Transaction date and time
    phone_number TEXT,                    -- Associated phone number
    balance_after REAL,                   -- Balance after transaction
    fee REAL DEFAULT 0,                   -- Transaction fee if applicable
    description TEXT,                     -- Additional transaction details
    agent_name TEXT,                      -- Agent name for withdrawals
    agent_phone TEXT,                     -- Agent phone number for withdrawals
    bundle_type TEXT,                     -- For internet/voice bundle purchases
    bundle_validity INTEGER,              -- Bundle validity in days
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Create transaction_types table to maintain valid transaction types
CREATE TABLE IF NOT EXISTS transaction_types (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    type_name TEXT UNIQUE NOT NULL,       -- Name of transaction type
    description TEXT,                     -- Description of the transaction type
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Create indexes for better query performance
CREATE INDEX IF NOT EXISTS idx_transactions_type ON transactions(type);
CREATE INDEX IF NOT EXISTS idx_transactions_date ON transactions(date);
CREATE INDEX IF NOT EXISTS idx_transactions_name ON transactions(name);
CREATE INDEX IF NOT EXISTS idx_transactions_phone ON transactions(phone_number);

-- Insert default transaction types
INSERT OR IGNORE INTO transaction_types (type_name, description) VALUES
    ('Incoming Money', 'Money received from other users'),
    ('Payment', 'Payments to code holders'),
    ('Transfer', 'Transfers to mobile numbers'),
    ('Bank Deposit', 'Money deposited from bank'),
    ('Airtime Bill Payment', 'Payments for airtime'),
    ('Cash Power Bill Payment', 'Payments for electricity'),
    ('Third Party Transaction', 'Transactions initiated by third parties'),
    ('Withdrawal', 'Cash withdrawals from agents'),
    ('Bank Transfer', 'Transfers to/from bank'),
    ('Internet Bundle', 'Internet bundle purchases'),
    ('Voice Bundle', 'Voice bundle purchases');

-- Create view for transaction statistics
CREATE VIEW IF NOT EXISTS transaction_stats AS
SELECT 
    type,
    COUNT(*) as transaction_count,
    SUM(amount) as total_amount,
    AVG(amount) as average_amount,
    MIN(amount) as min_amount,
    MAX(amount) as max_amount,
    COUNT(DISTINCT name) as unique_users
FROM transactions
GROUP BY type;

-- Create view for monthly transaction summaries
CREATE VIEW IF NOT EXISTS monthly_transactions AS
SELECT 
    strftime('%Y-%m', date) as month,
    type,
    COUNT(*) as transaction_count,
    SUM(amount) as total_amount
FROM transactions
GROUP BY strftime('%Y-%m', date), type;

-- Create trigger to update updated_at timestamp
CREATE TRIGGER IF NOT EXISTS update_transaction_timestamp 
AFTER UPDATE ON transactions
BEGIN
    UPDATE transactions SET updated_at = CURRENT_TIMESTAMP
    WHERE id = NEW.id;
END; 