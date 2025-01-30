# ChromaFinance

A sophisticated billing and financial management system powered by LangChain multi-agent AI system.

## Features

- Invoice Management
- Payment Processing
- Financial Reporting
- Multi-Agent AI System
- RESTful API
- Docker Support

## Prerequisites

- Docker and Docker Compose
- API Keys for:
  - OpenAI
  - Google AI
  - Anthropic (Claude)

## Quick Start with Docker

1. Clone the repository:
```bash
git clone https://github.com/Eblack17/ChromaFinance.git
cd ChromaFinance
```

2. Set up environment variables:
```bash
cp .env.example .env
# Edit .env with your API keys
```

3. Build and run with Docker Compose:
```bash
docker-compose up --build
```

The application will be available at http://localhost:8000

## API Endpoints

### Base Endpoints
- `GET /` - API information and available endpoints
- `POST /invoices` - Create new invoice
- `GET /invoices/<invoice_id>` - Get invoice details
- `PUT /invoices/<invoice_id>/status` - Update invoice status
- `GET /invoices/overdue` - Get overdue invoices
- `POST /payments` - Record payment
- `POST /reports` - Generate reports

### AI Agent Endpoints
- `POST /ai/analyze` - Financial analysis and insights
- `POST /ai/forecast` - Revenue forecasting
- `POST /ai/optimize` - Payment optimization suggestions
- `POST /ai/risk` - Risk assessment

## Development

### Running Tests
```bash
python test_api.py
```

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

3. Run the application:
```bash
python app.py
```

## Docker Commands

### Build the Image
```bash
docker build -t chromafinance .
```

### Run the Container
```bash
docker run -p 8000:8000 -d chromafinance
```

### Using Docker Compose
```bash
# Start services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

## License

MIT License

## Contributing

1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Create a new Pull Request 
