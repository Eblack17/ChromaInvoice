from typing import Dict, List, Optional
from datetime import datetime
import json
import os
import csv
from collections import defaultdict
from email_service import EmailService

class BillingDatabase:
    """Simple database interface for billing operations"""
    
    def __init__(self, data_dir: str = "data", smtp_config: Dict = None):
        self.data_dir = data_dir
        self._ensure_data_directory()
        self.email_service = EmailService(smtp_config)
        
    def _ensure_data_directory(self):
        """Create data directory if it doesn't exist"""
        if not os.path.exists(self.data_dir):
            os.makedirs(self.data_dir)
            os.makedirs(os.path.join(self.data_dir, "invoices"))
            os.makedirs(os.path.join(self.data_dir, "clients"))
            os.makedirs(os.path.join(self.data_dir, "payments"))
            os.makedirs(os.path.join(self.data_dir, "reports"))
        else:
            # Ensure all subdirectories exist
            for subdir in ["invoices", "clients", "payments", "reports"]:
                path = os.path.join(self.data_dir, subdir)
                if not os.path.exists(path):
                    os.makedirs(path)
    
    def create_invoice(self, invoice_data: Dict) -> str:
        """Create a new invoice and return its ID"""
        invoice_id = f"INV-{datetime.now().strftime('%Y%m%d-%H%M%S')}"
        invoice_data["invoice_id"] = invoice_id
        invoice_data["created_at"] = datetime.now().isoformat()
        invoice_data["status"] = "pending"
        
        with open(os.path.join(self.data_dir, "invoices", f"{invoice_id}.json"), "w") as f:
            json.dump(invoice_data, f, indent=2)
        
        # Send invoice email if client email is provided
        if "client_email" in invoice_data:
            self.email_service.send_invoice(
                invoice_data,
                invoice_data["client_email"],
                invoice_data["client_name"]
            )
        
        return invoice_id
    
    def get_invoice(self, invoice_id: str) -> Optional[Dict]:
        """Retrieve invoice by ID"""
        try:
            with open(os.path.join(self.data_dir, "invoices", f"{invoice_id}.json"), "r") as f:
                return json.load(f)
        except FileNotFoundError:
            return None
    
    def update_invoice_status(self, invoice_id: str, status: str) -> bool:
        """Update invoice status"""
        invoice = self.get_invoice(invoice_id)
        if invoice:
            invoice["status"] = status
            invoice["updated_at"] = datetime.now().isoformat()
            
            with open(os.path.join(self.data_dir, "invoices", f"{invoice_id}.json"), "w") as f:
                json.dump(invoice, f, indent=2)
            
            # Send payment reminder if status is overdue and client email exists
            if status == "overdue" and "client_email" in invoice:
                due_date = datetime.fromisoformat(invoice["due_date"])
                days_overdue = (datetime.now() - due_date).days
                self.email_service.send_payment_reminder(
                    invoice,
                    invoice["client_email"],
                    invoice["client_name"],
                    days_overdue
                )
            
            return True
        return False
    
    def get_overdue_invoices(self) -> List[Dict]:
        """Get all overdue invoices"""
        overdue = []
        invoices_dir = os.path.join(self.data_dir, "invoices")
        
        for filename in os.listdir(invoices_dir):
            if filename.endswith(".json"):
                with open(os.path.join(invoices_dir, filename), "r") as f:
                    invoice = json.load(f)
                    due_date = datetime.fromisoformat(invoice["due_date"])
                    if due_date < datetime.now() and invoice["status"] == "pending":
                        overdue.append(invoice)
        
        return overdue
    
    def record_payment(self, payment_data: Dict) -> str:
        """Record a payment"""
        payment_id = f"PAY-{datetime.now().strftime('%Y%m%d-%H%M%S')}"
        payment_data["payment_id"] = payment_id
        payment_data["recorded_at"] = datetime.now().isoformat()
        
        with open(os.path.join(self.data_dir, "payments", f"{payment_id}.json"), "w") as f:
            json.dump(payment_data, f, indent=2)
        
        # Update invoice status if payment is complete
        invoice_id = payment_data["invoice_id"]
        invoice = self.get_invoice(invoice_id)
        if invoice:
            if payment_data["amount"] >= invoice["amount"]:
                self.update_invoice_status(invoice_id, "paid")
                
                # Send payment confirmation if client email exists
                if "client_email" in invoice:
                    self.email_service.send_payment_confirmation(
                        payment_data,
                        invoice,
                        invoice["client_email"],
                        invoice["client_name"]
                    )
        
        return payment_id
    
    def generate_report(self, report_type: str, start_date: datetime, end_date: datetime, export_format: str = "json", email_to: Dict = None) -> Dict:
        """Generate financial report
        
        Args:
            report_type: Type of report ("revenue", "outstanding", "client_analysis", "service_metrics", "payment_trends")
            start_date: Start date for the report period
            end_date: End date for the report period
            export_format: Output format ("json" or "csv")
            email_to: Optional dict with keys 'email' and 'name' to send report via email
            
        Returns:
            Dict containing the report data
        """
        report = {
            "type": report_type,
            "period": {
                "start": start_date.isoformat(),
                "end": end_date.isoformat()
            },
            "generated_at": datetime.now().isoformat(),
            "data": {}
        }
        
        if report_type == "revenue":
            report["data"] = self._generate_revenue_report(start_date, end_date)
        elif report_type == "outstanding":
            report["data"] = self._generate_outstanding_report(start_date, end_date)
        elif report_type == "client_analysis":
            report["data"] = self._generate_client_analysis(start_date, end_date)
        elif report_type == "service_metrics":
            report["data"] = self._generate_service_metrics(start_date, end_date)
        elif report_type == "payment_trends":
            report["data"] = self._generate_payment_trends(start_date, end_date)
        
        # Export to CSV if requested
        if export_format == "csv":
            self._export_to_csv(report)
        
        # Send report via email if recipient is specified
        if email_to and "email" in email_to and "name" in email_to:
            self.email_service.send_report(
                report,
                email_to["email"],
                email_to["name"],
                attach_csv=(export_format == "csv")
            )
        
        return report
    
    def _generate_revenue_report(self, start_date: datetime, end_date: datetime) -> Dict:
        """Generate detailed revenue report"""
        total_revenue = 0
        paid_invoices = []
        monthly_revenue = defaultdict(float)
        payment_methods = defaultdict(float)
        
        for filename in os.listdir(os.path.join(self.data_dir, "payments")):
            if filename.endswith(".json"):
                with open(os.path.join(self.data_dir, "payments", filename), "r") as f:
                    payment = json.load(f)
                    payment_date = datetime.fromisoformat(payment["recorded_at"])
                    if start_date <= payment_date <= end_date:
                        amount = payment["amount"]
                        total_revenue += amount
                        paid_invoices.append(payment["invoice_id"])
                        
                        # Track monthly revenue
                        month_key = payment_date.strftime("%Y-%m")
                        monthly_revenue[month_key] += amount
                        
                        # Track payment methods
                        payment_methods[payment.get("payment_method", "unknown")] += amount
        
        return {
            "total_revenue": total_revenue,
            "paid_invoices_count": len(paid_invoices),
            "paid_invoices": paid_invoices,
            "monthly_breakdown": dict(monthly_revenue),
            "payment_methods": dict(payment_methods),
            "average_monthly_revenue": total_revenue / len(monthly_revenue) if monthly_revenue else 0
        }
    
    def _generate_outstanding_report(self, start_date: datetime, end_date: datetime) -> Dict:
        """Generate report on outstanding invoices"""
        outstanding_invoices = []
        total_outstanding = 0
        aging_buckets = {
            "30_days": 0,
            "60_days": 0,
            "90_days": 0,
            "90_plus_days": 0
        }
        
        for filename in os.listdir(os.path.join(self.data_dir, "invoices")):
            if filename.endswith(".json"):
                with open(os.path.join(self.data_dir, "invoices", filename), "r") as f:
                    invoice = json.load(f)
                    if invoice["status"] == "pending":
                        due_date = datetime.fromisoformat(invoice["due_date"])
                        if start_date <= due_date <= end_date:
                            days_overdue = (datetime.now() - due_date).days
                            amount = invoice["amount"]
                            
                            outstanding_invoices.append({
                                "invoice_id": invoice["invoice_id"],
                                "client_name": invoice["client_name"],
                                "amount": amount,
                                "days_overdue": days_overdue
                            })
                            
                            total_outstanding += amount
                            
                            # Categorize by aging
                            if days_overdue <= 30:
                                aging_buckets["30_days"] += amount
                            elif days_overdue <= 60:
                                aging_buckets["60_days"] += amount
                            elif days_overdue <= 90:
                                aging_buckets["90_days"] += amount
                            else:
                                aging_buckets["90_plus_days"] += amount
        
        return {
            "total_outstanding": total_outstanding,
            "outstanding_count": len(outstanding_invoices),
            "aging_analysis": aging_buckets,
            "outstanding_invoices": outstanding_invoices
        }
    
    def _generate_client_analysis(self, start_date: datetime, end_date: datetime) -> Dict:
        """Generate client-focused analysis"""
        client_metrics = defaultdict(lambda: {
            "total_spent": 0,
            "invoices_count": 0,
            "services_used": set(),
            "payment_history": []
        })
        
        # Analyze invoices and payments
        for filename in os.listdir(os.path.join(self.data_dir, "invoices")):
            if filename.endswith(".json"):
                with open(os.path.join(self.data_dir, "invoices", filename), "r") as f:
                    invoice = json.load(f)
                    invoice_date = datetime.fromisoformat(invoice["created_at"])
                    if start_date <= invoice_date <= end_date:
                        client_name = invoice["client_name"]
                        client_metrics[client_name]["invoices_count"] += 1
                        client_metrics[client_name]["services_used"].update(invoice["services"])
        
        # Add payment information
        for filename in os.listdir(os.path.join(self.data_dir, "payments")):
            if filename.endswith(".json"):
                with open(os.path.join(self.data_dir, "payments", filename), "r") as f:
                    payment = json.load(f)
                    payment_date = datetime.fromisoformat(payment["recorded_at"])
                    if start_date <= payment_date <= end_date:
                        invoice = self.get_invoice(payment["invoice_id"])
                        if invoice:
                            client_name = invoice["client_name"]
                            client_metrics[client_name]["total_spent"] += payment["amount"]
                            client_metrics[client_name]["payment_history"].append({
                                "date": payment["recorded_at"],
                                "amount": payment["amount"],
                                "method": payment.get("payment_method", "unknown")
                            })
        
        # Convert sets to lists for JSON serialization
        for client_data in client_metrics.values():
            client_data["services_used"] = list(client_data["services_used"])
        
        return {
            "client_metrics": dict(client_metrics),
            "total_active_clients": len(client_metrics),
            "average_client_spend": sum(c["total_spent"] for c in client_metrics.values()) / len(client_metrics) if client_metrics else 0
        }
    
    def _generate_service_metrics(self, start_date: datetime, end_date: datetime) -> Dict:
        """Generate metrics about services offered"""
        service_metrics = defaultdict(lambda: {
            "total_revenue": 0,
            "usage_count": 0,
            "clients": set()
        })
        
        for filename in os.listdir(os.path.join(self.data_dir, "invoices")):
            if filename.endswith(".json"):
                with open(os.path.join(self.data_dir, "invoices", filename), "r") as f:
                    invoice = json.load(f)
                    invoice_date = datetime.fromisoformat(invoice["created_at"])
                    if start_date <= invoice_date <= end_date:
                        # Assuming equal distribution of invoice amount across services
                        amount_per_service = invoice["amount"] / len(invoice["services"])
                        for service in invoice["services"]:
                            service_metrics[service]["total_revenue"] += amount_per_service
                            service_metrics[service]["usage_count"] += 1
                            service_metrics[service]["clients"].add(invoice["client_name"])
        
        # Convert sets to lists for JSON serialization
        for service_data in service_metrics.values():
            service_data["clients"] = list(service_data["clients"])
            service_data["average_revenue"] = service_data["total_revenue"] / service_data["usage_count"]
        
        return {
            "service_metrics": dict(service_metrics),
            "top_services": sorted(
                service_metrics.items(),
                key=lambda x: x[1]["total_revenue"],
                reverse=True
            )[:5]
        }
    
    def _generate_payment_trends(self, start_date: datetime, end_date: datetime) -> Dict:
        """Generate analysis of payment trends"""
        payment_trends = {
            "daily_volumes": defaultdict(float),
            "payment_methods": defaultdict(float),
            "average_payment_size": 0,
            "payment_timing": defaultdict(int)  # Days from invoice to payment
        }
        
        total_payments = 0
        total_amount = 0
        
        for filename in os.listdir(os.path.join(self.data_dir, "payments")):
            if filename.endswith(".json"):
                with open(os.path.join(self.data_dir, "payments", filename), "r") as f:
                    payment = json.load(f)
                    payment_date = datetime.fromisoformat(payment["recorded_at"])
                    if start_date <= payment_date <= end_date:
                        amount = payment["amount"]
                        total_payments += 1
                        total_amount += amount
                        
                        # Daily volume
                        date_key = payment_date.strftime("%Y-%m-%d")
                        payment_trends["daily_volumes"][date_key] += amount
                        
                        # Payment methods
                        method = payment.get("payment_method", "unknown")
                        payment_trends["payment_methods"][method] += amount
                        
                        # Payment timing
                        invoice = self.get_invoice(payment["invoice_id"])
                        if invoice:
                            invoice_date = datetime.fromisoformat(invoice["created_at"])
                            days_to_payment = (payment_date - invoice_date).days
                            payment_trends["payment_timing"][days_to_payment] += 1
        
        # Calculate averages and convert defaultdicts to regular dicts
        payment_trends["average_payment_size"] = total_amount / total_payments if total_payments > 0 else 0
        payment_trends["daily_volumes"] = dict(payment_trends["daily_volumes"])
        payment_trends["payment_methods"] = dict(payment_trends["payment_methods"])
        payment_trends["payment_timing"] = dict(payment_trends["payment_timing"])
        
        return payment_trends
    
    def _export_to_csv(self, report: Dict) -> None:
        """Export report data to CSV format"""
        report_type = report["type"]
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{report_type}_report_{timestamp}.csv"
        filepath = os.path.join(self.data_dir, "reports", filename)
        
        # Flatten the data structure for CSV export
        flattened_data = self._flatten_report_data(report["data"])
        
        if flattened_data:
            try:
                with open(filepath, 'w', newline='') as csvfile:
                    writer = csv.DictWriter(csvfile, fieldnames=flattened_data[0].keys())
                    writer.writeheader()
                    writer.writerows(flattened_data)
            except Exception as e:
                print(f"Error exporting to CSV: {str(e)}")
    
    def _flatten_report_data(self, data: Dict) -> List[Dict]:
        """Flatten nested report data for CSV export"""
        flattened = []
        
        if isinstance(data, dict):
            if "monthly_breakdown" in data:
                # Revenue report
                for month, amount in data["monthly_breakdown"].items():
                    flattened.append({
                        "month": month,
                        "revenue": amount,
                        "total_revenue": data["total_revenue"]
                    })
            elif "outstanding_invoices" in data:
                # Outstanding report
                flattened = data["outstanding_invoices"]
            elif "client_metrics" in data:
                # Client analysis
                for client, metrics in data["client_metrics"].items():
                    flattened.append({
                        "client_name": client,
                        "total_spent": metrics["total_spent"],
                        "invoices_count": metrics["invoices_count"],
                        "services": ", ".join(metrics["services_used"])
                    })
            elif "service_metrics" in data:
                # Service metrics
                for service, metrics in data["service_metrics"].items():
                    flattened.append({
                        "service": service,
                        "total_revenue": metrics["total_revenue"],
                        "usage_count": metrics["usage_count"],
                        "client_count": len(metrics["clients"])
                    })
            elif "daily_volumes" in data:
                # Payment trends
                for date, amount in data["daily_volumes"].items():
                    flattened.append({
                        "date": date,
                        "amount": amount,
                        "average_payment_size": data["average_payment_size"]
                    })
        
        return flattened 