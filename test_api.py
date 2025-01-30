import requests
import json
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# API base URL
BASE_URL = "http://localhost:8000"

def test_home():
    """Test home endpoint"""
    print("\n1. Testing Home Endpoint")
    response = requests.get(f"{BASE_URL}/")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    assert response.status_code == 200

def test_create_invoice():
    """Test invoice creation"""
    print("\n2. Testing Invoice Creation")
    invoice_data = {
        "client_name": "Test Client",
        "client_email": os.getenv("TEST_EMAIL"),
        "services": ["Web Design", "SEO Setup"],
        "amount": 2000,
        "due_date": (datetime.now() + timedelta(days=30)).isoformat()
    }
    
    response = requests.post(
        f"{BASE_URL}/invoices",
        json=invoice_data
    )
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    assert response.status_code == 201
    return response.json()["invoice_id"]

def test_get_invoice(invoice_id):
    """Test getting invoice by ID"""
    print("\n3. Testing Get Invoice")
    response = requests.get(f"{BASE_URL}/invoices/{invoice_id}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    assert response.status_code == 200

def test_update_invoice_status(invoice_id):
    """Test updating invoice status"""
    print("\n4. Testing Update Invoice Status")
    response = requests.put(
        f"{BASE_URL}/invoices/{invoice_id}/status",
        json={"status": "overdue"}
    )
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    assert response.status_code == 200

def test_get_overdue_invoices():
    """Test getting overdue invoices"""
    print("\n5. Testing Get Overdue Invoices")
    response = requests.get(f"{BASE_URL}/invoices/overdue")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    assert response.status_code == 200

def test_record_payment(invoice_id):
    """Test payment recording"""
    print("\n6. Testing Payment Recording")
    payment_data = {
        "invoice_id": invoice_id,
        "amount": 2000,
        "payment_method": "Credit Card"
    }
    
    response = requests.post(
        f"{BASE_URL}/payments",
        json=payment_data
    )
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    assert response.status_code == 201
    return response.json()["payment_id"]

def test_generate_reports():
    """Test report generation"""
    print("\n7. Testing Report Generation")
    report_types = ["revenue", "outstanding", "client_analysis", "service_metrics", "payment_trends"]
    
    for report_type in report_types:
        print(f"\n7.{report_types.index(report_type) + 1}. Testing {report_type} report")
        report_data = {
            "report_type": report_type,
            "start_date": (datetime.now() - timedelta(days=30)).isoformat(),
            "end_date": datetime.now().isoformat(),
            "export_format": "csv",
            "email_to": {
                "email": os.getenv("TEST_EMAIL"),
                "name": "Test User"
            }
        }
        
        response = requests.post(
            f"{BASE_URL}/reports",
            json=report_data
        )
        print(f"Response: {json.dumps(response.json(), indent=2)}")
        assert response.status_code == 200

def main():
    """Run all API tests"""
    print("Starting API Tests")
    print("=================")
    
    try:
        # Test basic endpoints
        test_home()
        
        # Test invoice workflow
        invoice_id = test_create_invoice()
        test_get_invoice(invoice_id)
        test_update_invoice_status(invoice_id)
        test_get_overdue_invoices()
        
        # Test payment
        payment_id = test_record_payment(invoice_id)
        
        # Test reports
        test_generate_reports()
        
        print("\nAll tests completed successfully!")
        
    except AssertionError:
        print("\nTest failed! Check the response above for details.")
    except Exception as e:
        print(f"\nError during testing: {str(e)}")

if __name__ == "__main__":
    main() 