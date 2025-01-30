from flask import Flask, request, jsonify
from flask_cors import CORS
from database import BillingDatabase
from datetime import datetime
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__)
CORS(app)

# Initialize database
db = BillingDatabase()

@app.route("/")
def home():
    """Home endpoint"""
    return jsonify({
        "message": "ChromaFinance Billing System API",
        "version": "1.0.0",
        "endpoints": [
            "/invoices",
            "/payments",
            "/reports"
        ]
    })

@app.route("/invoices", methods=["POST"])
def create_invoice():
    """Create a new invoice"""
    data = request.get_json()
    try:
        invoice_id = db.create_invoice(data)
        return jsonify({
            "message": "Invoice created successfully",
            "invoice_id": invoice_id
        }), 201
    except Exception as e:
        return jsonify({
            "error": str(e)
        }), 400

@app.route("/invoices/<invoice_id>", methods=["GET"])
def get_invoice(invoice_id):
    """Get invoice by ID"""
    invoice = db.get_invoice(invoice_id)
    if invoice:
        return jsonify(invoice)
    return jsonify({
        "error": "Invoice not found"
    }), 404

@app.route("/invoices/<invoice_id>/status", methods=["PUT"])
def update_invoice_status(invoice_id):
    """Update invoice status"""
    data = request.get_json()
    status = data.get("status")
    if not status:
        return jsonify({
            "error": "Status is required"
        }), 400
    
    success = db.update_invoice_status(invoice_id, status)
    if success:
        return jsonify({
            "message": "Invoice status updated successfully"
        })
    return jsonify({
        "error": "Invoice not found"
    }), 404

@app.route("/invoices/overdue", methods=["GET"])
def get_overdue_invoices():
    """Get all overdue invoices"""
    invoices = db.get_overdue_invoices()
    return jsonify(invoices)

@app.route("/payments", methods=["POST"])
def record_payment():
    """Record a payment"""
    data = request.get_json()
    try:
        payment_id = db.record_payment(data)
        return jsonify({
            "message": "Payment recorded successfully",
            "payment_id": payment_id
        }), 201
    except Exception as e:
        return jsonify({
            "error": str(e)
        }), 400

@app.route("/reports", methods=["POST"])
def generate_report():
    """Generate a financial report"""
    data = request.get_json()
    try:
        # Parse dates
        start_date = datetime.fromisoformat(data["start_date"])
        end_date = datetime.fromisoformat(data["end_date"])
        
        report = db.generate_report(
            report_type=data["report_type"],
            start_date=start_date,
            end_date=end_date,
            export_format=data.get("export_format", "json"),
            email_to=data.get("email_to")
        )
        return jsonify(report)
    except Exception as e:
        return jsonify({
            "error": str(e)
        }), 400

if __name__ == "__main__":
    port = int(os.getenv("PORT", 8000))
    app.run(host="0.0.0.0", port=port) 