# ChromaFinance

A modern, containerized billing and invoicing system built with Flask.

## Features

- Invoice Creation and Management
- Payment Processing
- Automated Payment Reminders
- Comprehensive Financial Reports
- RESTful API
- Docker Support

## Prerequisites

- Python 3.12+
- Docker (for containerized deployment)
- Git

## Installation

### Local Development

1. Clone the repository:
```bash
git clone https://github.com/Eblack17/ChromaFinance.git
cd ChromaFinance
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the application:
```bash
python app.py
```

### Docker Deployment

1. Build the Docker image:
```bash
docker build -t chromafinance .
```

2. Run the container:
```bash
docker run -d -p 8000:8000 chromafinance
```

## API Documentation

### Endpoints

- `GET /`: List available endpoints
- `POST /invoices`: Create a new invoice
- `GET /invoices/<invoice_id>`: Get invoice details
- `PUT /invoices/<invoice_id>/status`: Update invoice status
- `GET /invoices/overdue`: Get overdue invoices
- `POST /payments`: Record a payment
- `POST /reports`: Generate financial reports

## Testing

Run the test suite:
```bash
python test_api.py
```

## Environment Variables

Create a `.env` file with the following variables:
```
DATA_DIR=./data
FLASK_APP=app.py
FLASK_ENV=production
```

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details. 
