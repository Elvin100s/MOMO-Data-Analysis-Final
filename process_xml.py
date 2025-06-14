"""
Mobile Money Transaction XML Processor

This module handles the extraction and processing of Mobile Money transactions from XML SMS data.
It parses the XML file, extracts transaction details, and categorizes them into different types.

Transaction Types:
- Incoming Money: Money received from other users
- Payment: Payments to code holders
- Transfer: Transfers to mobile numbers
- Bank Deposit: Money deposited from bank
- Withdrawal: Cash withdrawals from agents
"""

import xml.etree.ElementTree as ET
from datetime import datetime
from database import insert_transaction

def parse_sms_body(body):
    """
    Parse the SMS body text to extract transaction details.
    
    Args:
        body (str): The SMS message body text
        
    Returns:
        tuple: (name, amount, trans_type, phone_number, balance_after)
            - name: Name of sender/recipient
            - amount: Transaction amount
            - trans_type: Type of transaction
            - phone_number: Phone number if available
            - balance_after: Balance after transaction
    """
    # Initialize default values
    name = "Unknown"
    amount = 0
    trans_type = "Other"
    phone_number = ""
    balance_after = 0
    
    try:
        # Pattern 1: Incoming money
        if "received" in body and "RWF from" in body:
            trans_type = "Incoming"
            parts = body.split("RWF from")
            amount = float(parts[0].split("received")[1].strip().replace(",", ""))
            name = parts[1].split("(")[0].strip()
            
            # Extract phone number if available
            if "(" in parts[1] and ")" in parts[1]:
                phone_number = parts[1].split("(")[1].split(")")[0]
            
            # Extract balance
            if "Your new balance:" in body:
                balance_str = body.split("Your new balance:")[1].split("RWF")[0].strip()
                balance_after = float(balance_str.replace(",", ""))
                
        # Pattern 2: Payment to someone
        elif "Your payment of" in body and "RWF to" in body:
            trans_type = "Payment"
            parts = body.split("RWF to")
            amount = float(parts[0].split("Your payment of")[1].strip().replace(",", ""))
            name = parts[1].split()[0].strip() + " " + parts[1].split()[1].strip()
            
            # Extract balance
            if "Your new balance:" in body:
                balance_str = body.split("Your new balance:")[1].split("RWF")[0].strip()
                balance_after = float(balance_str.replace(",", ""))
                
        # Pattern 3: Transfer to mobile number
        elif "RWF transferred to" in body:
            trans_type = "Transfer"
            parts = body.split("RWF transferred to")
            amount = float(parts[0].split("*S*")[1].strip().replace(",", ""))
            name = parts[1].split("(")[0].strip()
            
            # Extract phone number
            if "(" in body and ")" in body:
                phone_number = body.split("(")[1].split(")")[0]
            
            # Extract balance
            if "New balance:" in body:
                balance_str = body.split("New balance:")[1].split("RWF")[0].strip()
                balance_after = float(balance_str.replace(",", ""))
                
        # Pattern 4: Bank deposit
        elif "bank deposit of" in body and "RWF has been added" in body:
            trans_type = "Bank Deposit"
            parts = body.split("bank deposit of")
            amount = float(parts[1].split("RWF")[0].strip().replace(",", ""))
            name = "Bank"
            
            # Extract balance
            if "NEW BALANCE :" in body:
                balance_str = body.split("NEW BALANCE :")[1].split("RWF")[0].strip()
                balance_after = float(balance_str.replace(",", ""))
                
        # Pattern 5: Withdrawal from agent
        elif "withdrawn" in body and "RWF from" in body:
            trans_type = "Withdrawal"
            parts = body.split("withdrawn")
            amount = float(parts[1].split("RWF")[0].strip().replace(",", ""))
            name = parts[0].split("You")[1].strip().split()[0]
            
            # Extract balance
            if "Your new balance:" in body:
                balance_str = body.split("Your new balance:")[1].split("RWF")[0].strip()
                balance_after = float(balance_str.replace(",", ""))
                
    except Exception as e:
        print(f"Error parsing message: {e}")
        print(f"Message content: {body}")
    
    return name, amount, trans_type, phone_number, balance_after

def process_xml_file(xml_file):
    """
    Process the XML file containing SMS messages and store transactions in the database.
    
    Args:
        xml_file (str): Path to the XML file containing SMS messages
        
    The function:
    1. Parses the XML file
    2. Extracts transaction details from each SMS
    3. Stores valid transactions in the database
    """
    tree = ET.parse(xml_file)
    root = tree.getroot()
    
    for sms in root.findall('sms'):
        body = sms.get('body')
        date = sms.get('readable_date')
        
        name, amount, trans_type, phone_number, balance_after = parse_sms_body(body)
        
        if amount > 0:  # Only insert if we found an amount
            insert_transaction(
                name=name,
                amount=amount,
                trans_type=trans_type,
                date=date,
                phone_number=phone_number,
                balance_after=balance_after
            )

if __name__ == "__main__":
    from database import create_database
    create_database()
    process_xml_file("modified_sms_v2.xml")
    print("Data processing complete!")