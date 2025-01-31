# ChromaInvoice

A modern, containerized billing and invoicing system built with Flask.

## Features

- Invoice Generation and Management
- Payment Processing
- Financial Report Generation
- RESTful API Interface
- AI-Powered Billing Agent
- Containerized Deployment
- Data Persistence

## Components

### 1. RESTful API Server
The system provides a comprehensive REST API for managing invoices, payments, and reports. All endpoints return JSON responses and use standard HTTP methods.

### 2. AI Billing Agent
An intelligent agent powered by Google's Gemini Pro model that can understand natural language commands for invoice management and financial operations.

## API Endpoints

### Core Endpoints
- `GET /` - API information and documentation
- `GET /health` - Health check endpoint

### Invoice Operations
- `POST /api/invoices` - Create new invoice
- `GET /api/invoices/<id>` - Get invoice details
- `PUT /api/invoices/<id>/status` - Update invoice status
- `GET /api/invoices/overdue` - Get overdue invoices

### Payment Operations
- `POST /api/payments` - Record payment

### Report Operations
- `POST /api/reports` - Generate financial reports
- `GET /api/reports/types` - List available report types

## Setup and Installation

### Prerequisites

- Docker
- Docker Compose
- Python 3.9+
- Git

### Running with Docker

1. Clone the repository:
   ```bash
   git clone https://github.com/Eblack17/ChromaInvoice.git
   cd ChromaInvoice
   ```

2. Create a `.env` file with your configuration:
   ```bash
   cp .env.example .env
   # Edit .env with your settings
   ```

3. Build and run with Docker Compose:
   ```bash
   docker-compose up --build
   ```

The API will be available at `http://localhost:8080`

### Local Development

1. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Run the API server:
   ```bash
   flask run
   ```

4. Run the AI Billing Agent:
   ```bash
   python run_agent.py
   ```

## API Usage Examples

### Creating an Invoice
```bash
curl -X POST http://localhost:8080/api/invoices \
  -H "Content-Type: application/json" \
  -d '{
    "client_name": "TechCorp",
    "services": ["Web Development"],
    "amount": 1500.00,
    "due_date": "2024-02-28"
  }'
```

### Recording a Payment
```bash
curl -X POST http://localhost:8080/api/payments \
  -H "Content-Type: application/json" \
  -d '{
    "invoice_id": "INV-20240130-123456",
    "amount": 1500.00,
    "payment_method": "credit_card"
  }'
```

### Generating a Report
```bash
curl -X POST http://localhost:8080/api/reports \
  -H "Content-Type: application/json" \
  -d '{
    "report_type": "revenue",
    "start_date": "2024-01-01",
    "end_date": "2024-12-31"
  }'
```

## Environment Variables

Required environment variables in `.env` file:

```env
# API Configuration
FLASK_APP=app.py
FLASK_ENV=development  # Use 'production' in production
FLASK_DEBUG=True      # Set to False in production
PORT=8080             # Required for Cloud Run compatibility

# Google AI Configuration
GOOGLE_API_KEY=your_api_key_here

# SMTP Configuration (Optional)
SMTP_HOST=smtp.example.com
SMTP_PORT=587
SMTP_USERNAME=your_username
SMTP_PASSWORD=your_password
FROM_EMAIL=billing@yourcompany.com
FROM_NAME="Your Company Billing"
```

## Security Considerations

1. Never commit sensitive information (API keys, passwords) to the repository
2. Use environment variables for configuration
3. Set appropriate CORS policies in production
4. Use HTTPS in production
5. Implement proper authentication and authorization

## License

MIT License

## Author

Eric Black 
