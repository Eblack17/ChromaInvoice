# Billing System API

A Flask-based RESTful API for managing invoices, payments, and generating financial reports.

## Features

- Invoice Management (Create, Read, Update)
- Payment Processing
- Comprehensive Financial Reports
  - Revenue Reports
  - Outstanding Invoices
  - Client Analysis
  - Service Metrics
  - Payment Trends
- Email Notifications
- Data Persistence
- Error Handling

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/billing-system.git
cd billing-system
```

2. Create a virtual environment and activate it:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create a `.env` file with your configuration:
```
TEST_EMAIL=your-email@example.com
```

## Usage

1. Start the server:
```bash
python app.py
```

2. The API will be available at `http://localhost:8000`

## API Endpoints

- `GET /` - List available endpoints
- `POST /invoices` - Create a new invoice
- `GET /invoices/<invoice_id>` - Get invoice details
- `PUT /invoices/<invoice_id>/status` - Update invoice status
- `GET /invoices/overdue` - Get overdue invoices
- `POST /payments` - Record a payment
- `POST /reports` - Generate financial reports

## Testing

Run the test suite:
```bash
python test_api.py
```

## Production Deployment

For production deployment, use Gunicorn:
```bash
gunicorn -w 4 -b 0.0.0.0:8000 app:app
```

## License

MIT License

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request 
