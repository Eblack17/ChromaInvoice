# Chromapages Billing System

A comprehensive billing system for managing invoices, payments, and financial reporting.

## Features

### Core Billing Features
- Invoice generation and management
- Payment processing and tracking
- Automated payment reminders
- Financial record keeping

### Advanced Reporting
- Revenue reports with monthly breakdowns
- Outstanding invoice analysis with aging buckets
- Client spending analysis and metrics
- Service usage and revenue metrics
- Payment trend analysis
- CSV export capability for all reports

### Email Notifications
- Invoice notifications to clients
- Payment reminders (gentle, urgent, and final notices)
- Payment confirmations
- Report delivery via email
- CSV report attachments

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Configure environment variables:
```bash
# SMTP Configuration
SMTP_HOST=smtp.example.com
SMTP_PORT=587
SMTP_USERNAME=your_username
SMTP_PASSWORD=your_password
FROM_EMAIL=billing@yourcompany.com
FROM_NAME="Your Company Billing"

# For testing
TEST_EMAIL=test@example.com
```

3. Create data directory:
```bash
mkdir -p data/{invoices,clients,payments,reports}
```

## Usage

### Basic Operations

1. Create an invoice:
```python
from database import BillingDatabase

db = BillingDatabase()
invoice_data = {
    "client_name": "Client Name",
    "client_email": "client@example.com",
    "services": ["Web Design", "SEO Setup"],
    "amount": 2000,
    "due_date": "2024-03-01"
}
invoice_id = db.create_invoice(invoice_data)
```

2. Record a payment:
```python
payment_data = {
    "invoice_id": invoice_id,
    "amount": 2000,
    "payment_method": "Credit Card"
}
payment_id = db.record_payment(payment_data)
```

### Generating Reports

1. Revenue Report:
```python
from datetime import datetime, timedelta

start_date = datetime.now() - timedelta(days=30)
end_date = datetime.now()

report = db.generate_report(
    "revenue",
    start_date,
    end_date,
    export_format="csv",
    email_to={
        "email": "manager@example.com",
        "name": "Finance Manager"
    }
)
```

2. Client Analysis:
```python
report = db.generate_report(
    "client_analysis",
    start_date,
    end_date,
    export_format="csv"
)
```

### Available Report Types
1. `revenue` - Revenue analysis and trends
2. `outstanding` - Outstanding invoice analysis
3. `client_analysis` - Client spending patterns
4. `service_metrics` - Service popularity and revenue
5. `payment_trends` - Payment method analysis

## Testing

Run the test suites:

1. Basic functionality tests:
```bash
python test_billing.py
```

2. Report generation tests:
```bash
python test_reports.py
```

3. Email notification tests:
```bash
python test_email.py
```

## Data Storage

All data is stored in JSON format in the following structure:

```
data/
├── invoices/
│   └── INV-YYYYMMDD-HHMMSS.json
├── payments/
│   └── PAY-YYYYMMDD-HHMMSS.json
├── clients/
│   └── client_data.json
└── reports/
    └── report_type_YYYYMMDD_HHMMSS.csv
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details. 