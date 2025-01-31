from flask import Flask, request, jsonify
from flask_cors import CORS
from database import BillingDatabase
from datetime import datetime, timedelta
from dotenv import load_dotenv
import os
import json
from dateutil.parser import parse

# Load environment variables
load_dotenv()

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Initialize database lazily
db = None

def get_db():
    """Get database instance"""
    global db
    if db is None:
        db = app.config.get('DATABASE') or BillingDatabase()
    return db

# Error handlers
@app.errorhandler(404)
def not_found_error(error):
    return jsonify({
        "error": "Resource not found",
        "message": str(error)
    }), 404

@app.errorhandler(400)
def bad_request_error(error):
    return jsonify({
        "error": "Bad request",
        "message": str(error)
    }), 400

@app.errorhandler(500)
def internal_error(error):
    return jsonify({
        "error": "Internal server error",
        "message": str(error)
    }), 500

# Health check endpoint - Moved to top priority
@app.route('/health', methods=['GET'])
def health_check():
    """Quick health check endpoint"""
    return jsonify({
        "status": "healthy",
        "timestamp": datetime.now().isoformat()
    })

# Root endpoint
@app.route('/', methods=['GET'])
def root():
    """Root endpoint with API information"""
    return jsonify({
        "name": "Chromapages Billing API",
        "version": "1.0.0",
        "endpoints": {
            "health": "/health",
            "invoices": {
                "create": "POST /api/invoices",
                "get": "GET /api/invoices/<id>",
                "update_status": "PUT /api/invoices/<id>/status",
                "get_overdue": "GET /api/invoices/overdue"
            },
            "payments": {
                "create": "POST /api/payments"
            },
            "reports": {
                "generate": "POST /api/reports",
                "types": "GET /api/reports/types"
            }
        }
    })

# Invoice endpoints
@app.route('/api/invoices', methods=['POST'])
def create_invoice():
    """Create a new invoice"""
    try:
        data = request.get_json()
        required_fields = ["client_name", "services", "amount"]
        
        # Validate required fields
        missing_fields = [field for field in required_fields if field not in data]
        if missing_fields:
            return jsonify({
                "error": f"Missing required fields: {', '.join(missing_fields)}"
            }), 400
        
        # Set due date if not provided
        if "due_date" not in data:
            data["due_date"] = (datetime.now() + timedelta(days=30)).isoformat()
        
        invoice_id = get_db().create_invoice(data)
        return jsonify({
            "message": "Invoice created successfully",
            "invoice_id": invoice_id
        })
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/invoices/<invoice_id>', methods=['GET'])
def get_invoice(invoice_id):
    """Get invoice details"""
    try:
        invoice = get_db().get_invoice(invoice_id)
        if invoice:
            return jsonify(invoice)
        return jsonify({"error": "Invoice not found"}), 404
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/invoices/<invoice_id>/status', methods=['PUT'])
def update_invoice_status(invoice_id):
    """Update invoice status"""
    try:
        data = request.get_json()
        if "status" not in data:
            return jsonify({"error": "Status field is required"}), 400
        
        success = get_db().update_invoice_status(invoice_id, data["status"])
        if success:
            return jsonify({"message": "Invoice status updated successfully"})
        return jsonify({"error": "Invoice not found"}), 404
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/invoices/overdue', methods=['GET'])
def get_overdue_invoices():
    """Get all overdue invoices"""
    try:
        overdue = get_db().get_overdue_invoices()
        return jsonify({
            "count": len(overdue),
            "invoices": overdue
        })
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Payment endpoints
@app.route('/api/payments', methods=['POST'])
def record_payment():
    """Record a payment"""
    try:
        data = request.get_json()
        required_fields = ["invoice_id", "amount", "payment_method"]
        
        # Validate required fields
        missing_fields = [field for field in required_fields if field not in data]
        if missing_fields:
            return jsonify({
                "error": f"Missing required fields: {', '.join(missing_fields)}"
            }), 400
        
        payment_id = get_db().record_payment(data)
        return jsonify({
            "message": "Payment recorded successfully",
            "payment_id": payment_id
        })
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Report endpoints
@app.route('/api/reports', methods=['POST'])
def generate_report():
    """Generate a financial report"""
    try:
        data = request.get_json()
        required_fields = ["report_type", "start_date", "end_date"]
        
        # Validate required fields
        missing_fields = [field for field in required_fields if field not in data]
        if missing_fields:
            return jsonify({
                "error": f"Missing required fields: {', '.join(missing_fields)}"
            }), 400
        
        # Parse dates
        try:
            start_date = parse(data["start_date"])
            end_date = parse(data["end_date"])
        except ValueError:
            return jsonify({
                "error": "Invalid date format. Use ISO format (YYYY-MM-DD)"
            }), 400
        
        # Optional parameters
        export_format = data.get("export_format", "json")
        email_to = data.get("email_to")
        
        report = get_db().generate_report(
            data["report_type"],
            start_date,
            end_date,
            export_format,
            email_to
        )
        
        return jsonify(report)
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/reports/types', methods=['GET'])
def get_report_types():
    """Get available report types"""
    return jsonify({
        "report_types": [
            {
                "id": "revenue",
                "name": "Revenue Report",
                "description": "Revenue analysis and trends"
            },
            {
                "id": "outstanding",
                "name": "Outstanding Invoice Report",
                "description": "Analysis of outstanding invoices"
            },
            {
                "id": "client_analysis",
                "name": "Client Analysis Report",
                "description": "Client spending patterns and metrics"
            },
            {
                "id": "service_metrics",
                "name": "Service Metrics Report",
                "description": "Service popularity and revenue analysis"
            },
            {
                "id": "payment_trends",
                "name": "Payment Trends Report",
                "description": "Payment method analysis and trends"
            }
        ]
    })

if __name__ == '__main__':
    # Ensure data directory exists
    if not os.path.exists('data'):
        os.makedirs('data')
        for subdir in ['invoices', 'clients', 'payments', 'reports']:
            os.makedirs(os.path.join('data', subdir))
    
    # Run the application
    port = int(os.getenv('PORT', 8080))
    app.run(
        host='0.0.0.0',  # Always bind to all interfaces
        port=port,
        debug=os.getenv('FLASK_DEBUG', 'False').lower() == 'true'
    ) 

