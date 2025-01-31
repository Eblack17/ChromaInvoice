# ChromaInvoice

A modern, containerized billing and invoicing system built with Flask.

## Features

- Invoice Generation and Management
- Payment Processing
- Financial Report Generation
- RESTful API Interface
- Containerized Deployment
- Data Persistence

## API Endpoints

- `GET /` - API information and documentation
- `GET /health` - Health check endpoint
- `POST /api/invoices` - Create new invoice
- `GET /api/invoices/<id>` - Get invoice details
- `PUT /api/invoices/<id>/status` - Update invoice status
- `GET /api/invoices/overdue` - Get overdue invoices
- `POST /api/payments` - Record payment
- `POST /api/reports` - Generate financial reports
- `GET /api/reports/types` - List available report types

## Setup and Installation

### Prerequisites

- Docker
- Docker Compose

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

The API will be available at `http://localhost:5000`

## Development

### Local Setup

1. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Run the application:
   ```bash
   flask run
   ```

## License

MIT License

## Author

Eric Black 
