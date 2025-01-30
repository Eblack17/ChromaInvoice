from database import BillingDatabase
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv

def main():
    """Main function to test the billing system"""
    # Load environment variables
    load_dotenv()
    
    print("ChromaFinance Billing System Test")
    print("=================================")
    
    # Initialize database
    db = BillingDatabase()
    
    # Test 1: Create Invoice
    print("\n1. Creating Test Invoice")
    invoice_data = {
        "client_name": "Test Client",
        "client_email": os.getenv("TEST_EMAIL"),
        "services": ["Web Design", "SEO Setup"],
        "amount": 2000,
        "due_date": (datetime.now() + timedelta(days=30)).isoformat()
    }
    invoice_id = db.create_invoice(invoice_data)
    print(f"Created invoice: {invoice_id}")
    
    # Test 2: Record Payment
    print("\n2. Recording Payment")
    payment_data = {
        "invoice_id": invoice_id,
        "amount": 2000,
        "payment_method": "Credit Card"
    }
    payment_id = db.record_payment(payment_data)
    print(f"Recorded payment: {payment_id}")
    
    # Test 3: Generate Reports
    print("\n3. Generating Reports")
    start_date = datetime.now() - timedelta(days=30)
    end_date = datetime.now() + timedelta(days=30)
    
    # Revenue Report
    print("\na. Revenue Report")
    revenue_report = db.generate_report(
        "revenue",
        start_date,
        end_date,
        export_format="csv",
        email_to={
            "email": os.getenv("TEST_EMAIL"),
            "name": "Test User"
        }
    )
    print("Revenue report generated and emailed")
    
    # Outstanding Report
    print("\nb. Outstanding Report")
    outstanding_report = db.generate_report(
        "outstanding",
        start_date,
        end_date
    )
    print("Outstanding report generated")
    
    # Client Analysis
    print("\nc. Client Analysis")
    client_report = db.generate_report(
        "client_analysis",
        start_date,
        end_date,
        export_format="csv"
    )
    print("Client analysis report generated")
    
    # Service Metrics
    print("\nd. Service Metrics")
    service_report = db.generate_report(
        "service_metrics",
        start_date,
        end_date
    )
    print("Service metrics report generated")
    
    # Payment Trends
    print("\ne. Payment Trends")
    trends_report = db.generate_report(
        "payment_trends",
        start_date,
        end_date,
        export_format="csv"
    )
    print("Payment trends report generated")
    
    print("\nAll tests completed successfully!")
    print("Check your email for notifications and reports.")

if __name__ == "__main__":
    main() 