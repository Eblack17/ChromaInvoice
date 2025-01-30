from billing_agent import BillingAgent
from database import BillingDatabase
import json
from datetime import datetime, timedelta

def test_direct_functionality():
    """Test the billing agent's functionality directly"""
    print("Starting direct functionality tests...")
    
    # Initialize the agent and database
    agent = BillingAgent()
    db = BillingDatabase()
    
    # Test 1: Create Invoice
    print("\n1. Testing Invoice Creation")
    invoice_data = {
        "client_name": "TechCorp",
        "services": ["Web Design", "SEO Setup"],
        "amount": 2000,
        "due_date": 30
    }
    
    create_tool = agent._create_invoice_tool()
    result = create_tool(json.dumps(invoice_data))
    print(f"Result: {result}")
    
    # Extract invoice ID from result
    invoice_id = result.split("Invoice ")[1].split(" generated")[0]
    
    # Test 2: Track Invoice
    print("\n2. Testing Invoice Tracking")
    track_tool = agent._track_invoice_tool()
    result = track_tool(invoice_id)
    print(f"Result: {result}")
    
    # Test 3: Record Payment
    print("\n3. Testing Payment Recording")
    payment_data = {
        "invoice_id": invoice_id,
        "amount": 2000,
        "payment_method": "Credit Card"
    }
    
    payment_tool = agent._record_payment_tool()
    result = payment_tool(json.dumps(payment_data))
    print(f"Result: {result}")
    
    # Test 4: Generate Report
    print("\n4. Testing Report Generation")
    report_data = {
        "report_type": "revenue",
        "start_date": (datetime.now() - timedelta(days=30)).isoformat(),
        "end_date": datetime.now().isoformat()
    }
    
    report_tool = agent._generate_report_tool()
    result = report_tool(json.dumps(report_data))
    print(f"Result: {result}")
    
    # Test 5: Payment Reminder
    print("\n5. Testing Payment Reminder")
    reminder_data = {
        "invoice_id": invoice_id
    }
    
    reminder_tool = agent._payment_reminder_tool()
    result = reminder_tool(json.dumps(reminder_data))
    print(f"Result: {result}")

if __name__ == "__main__":
    test_direct_functionality() 