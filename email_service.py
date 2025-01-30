from typing import List, Dict, Optional
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
import os
from datetime import datetime
import json

class EmailService:
    """Email service for sending billing notifications"""
    
    def __init__(self, smtp_config: Dict = None):
        """Initialize email service
        
        Args:
            smtp_config: Dictionary containing SMTP configuration
                Required keys: host, port, username, password, use_tls
        """
        self.config = smtp_config or {
            "host": os.getenv("SMTP_HOST", "smtp.gmail.com"),
            "port": int(os.getenv("SMTP_PORT", "587")),
            "username": os.getenv("SMTP_USERNAME", ""),
            "password": os.getenv("SMTP_PASSWORD", ""),
            "use_tls": True,
            "from_email": os.getenv("FROM_EMAIL", "billing@chromapages.com"),
            "from_name": os.getenv("FROM_NAME", "Chromapages Billing")
        }
    
    def send_invoice(self, invoice: Dict, to_email: str, to_name: str) -> bool:
        """Send invoice notification email
        
        Args:
            invoice: Invoice data dictionary
            to_email: Recipient email address
            to_name: Recipient name
            
        Returns:
            bool: True if email was sent successfully
        """
        subject = f"Invoice {invoice['invoice_id']} from Chromapages"
        
        # Create email body
        body = f"""Dear {to_name},

Thank you for choosing Chromapages. Please find your invoice details below:

Invoice Number: {invoice['invoice_id']}
Date: {invoice['created_at']}
Due Date: {invoice['due_date']}
Amount: ${invoice['amount']:.2f}

Services:
{self._format_services(invoice['services'])}

To make a payment or view your invoice online, please visit our client portal.

If you have any questions, please don't hesitate to contact us.

Best regards,
Chromapages Billing Team"""
        
        return self._send_email(to_email, subject, body)
    
    def send_payment_reminder(self, invoice: Dict, to_email: str, to_name: str, days_overdue: int) -> bool:
        """Send payment reminder email
        
        Args:
            invoice: Invoice data dictionary
            to_email: Recipient email address
            to_name: Recipient name
            days_overdue: Number of days the invoice is overdue
            
        Returns:
            bool: True if email was sent successfully
        """
        subject = f"Payment Reminder - Invoice {invoice['invoice_id']}"
        
        urgency = "gentle" if days_overdue <= 30 else "urgent" if days_overdue <= 60 else "final"
        
        # Create email body based on urgency
        if urgency == "gentle":
            body = f"""Dear {to_name},

This is a friendly reminder that payment for invoice {invoice['invoice_id']} ({invoice['created_at']}) 
for ${invoice['amount']:.2f} is now {days_overdue} days overdue.

If you have already made the payment, please disregard this notice.
If not, we would appreciate your prompt attention to this matter.

You can make payment through our client portal or contact us for assistance.

Best regards,
Chromapages Billing Team"""
        
        elif urgency == "urgent":
            body = f"""Dear {to_name},

We notice that invoice {invoice['invoice_id']} for ${invoice['amount']:.2f} remains unpaid 
and is now {days_overdue} days overdue.

Please arrange for immediate payment or contact us if you are experiencing any difficulties.
Failure to respond may result in service interruption.

Invoice Details:
- Invoice Number: {invoice['invoice_id']}
- Original Due Date: {invoice['due_date']}
- Amount Due: ${invoice['amount']:.2f}

Best regards,
Chromapages Billing Team"""
        
        else:  # final notice
            body = f"""Dear {to_name},

FINAL NOTICE

Invoice {invoice['invoice_id']} for ${invoice['amount']:.2f} is severely overdue 
({days_overdue} days).

If payment is not received within 7 days, we will have no choice but to:
1. Suspend all services
2. Refer the matter to our collections department
3. Apply late payment penalties as per our terms of service

To avoid these measures, please make immediate payment or contact us to discuss 
payment arrangements.

Best regards,
Chromapages Billing Team"""
        
        return self._send_email(to_email, subject, body)
    
    def send_payment_confirmation(self, payment: Dict, invoice: Dict, to_email: str, to_name: str) -> bool:
        """Send payment confirmation email
        
        Args:
            payment: Payment data dictionary
            invoice: Related invoice data
            to_email: Recipient email address
            to_name: Recipient name
            
        Returns:
            bool: True if email was sent successfully
        """
        subject = f"Payment Confirmation - Invoice {invoice['invoice_id']}"
        
        body = f"""Dear {to_name},

Thank you for your payment. This email confirms that we have received your payment 
for invoice {invoice['invoice_id']}.

Payment Details:
- Amount: ${payment['amount']:.2f}
- Date: {payment['recorded_at']}
- Method: {payment.get('payment_method', 'Not specified')}
- Transaction ID: {payment['payment_id']}

Original Invoice Details:
- Invoice Number: {invoice['invoice_id']}
- Invoice Date: {invoice['created_at']}
- Services: 
{self._format_services(invoice['services'])}

Thank you for your business!

Best regards,
Chromapages Billing Team"""
        
        return self._send_email(to_email, subject, body)
    
    def send_report(self, report: Dict, to_email: str, to_name: str, attach_csv: bool = False) -> bool:
        """Send report email
        
        Args:
            report: Report data dictionary
            to_email: Recipient email address
            to_name: Recipient name
            attach_csv: Whether to attach CSV version of report
            
        Returns:
            bool: True if email was sent successfully
        """
        report_type = report['type'].replace('_', ' ').title()
        subject = f"{report_type} Report - {report['period']['start']} to {report['period']['end']}"
        
        # Create email body with report summary
        body = f"""Dear {to_name},

Please find attached the {report_type} Report for the period:
{report['period']['start']} to {report['period']['end']}

Report Summary:
{self._format_report_summary(report)}

The complete report is attached in CSV format.

Best regards,
Chromapages Billing Team"""
        
        attachments = []
        if attach_csv:
            # Create CSV attachment
            csv_filename = f"{report['type']}_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
            csv_path = os.path.join("data", "reports", csv_filename)
            if os.path.exists(csv_path):
                with open(csv_path, 'rb') as f:
                    csv_attachment = MIMEApplication(f.read(), _subtype='csv')
                    csv_attachment.add_header('Content-Disposition', 'attachment', filename=csv_filename)
                    attachments.append(csv_attachment)
        
        return self._send_email(to_email, subject, body, attachments)
    
    def _send_email(self, to_email: str, subject: str, body: str, attachments: List = None) -> bool:
        """Send email using SMTP
        
        Args:
            to_email: Recipient email address
            subject: Email subject
            body: Email body text
            attachments: List of email attachments
            
        Returns:
            bool: True if email was sent successfully
        """
        try:
            msg = MIMEMultipart()
            msg['From'] = f"{self.config['from_name']} <{self.config['from_email']}>"
            msg['To'] = to_email
            msg['Subject'] = subject
            
            msg.attach(MIMEText(body, 'plain'))
            
            if attachments:
                for attachment in attachments:
                    msg.attach(attachment)
            
            with smtplib.SMTP(self.config['host'], self.config['port']) as server:
                if self.config['use_tls']:
                    server.starttls()
                
                if self.config['username'] and self.config['password']:
                    server.login(self.config['username'], self.config['password'])
                
                server.send_message(msg)
            
            return True
            
        except Exception as e:
            print(f"Error sending email: {str(e)}")
            return False
    
    def _format_services(self, services: List[str]) -> str:
        """Format services list for email body"""
        return "\n".join(f"- {service}" for service in services)
    
    def _format_report_summary(self, report: Dict) -> str:
        """Format report summary for email body"""
        summary = []
        data = report['data']
        
        if report['type'] == 'revenue':
            summary.extend([
                f"Total Revenue: ${data['total_revenue']:.2f}",
                f"Paid Invoices: {data['paid_invoices_count']}",
                f"Average Monthly Revenue: ${data['average_monthly_revenue']:.2f}"
            ])
        
        elif report['type'] == 'outstanding':
            summary.extend([
                f"Total Outstanding: ${data['total_outstanding']:.2f}",
                f"Outstanding Invoices: {data['outstanding_count']}",
                "\nAging Analysis:",
                f"- 30 Days: ${data['aging_analysis']['30_days']:.2f}",
                f"- 60 Days: ${data['aging_analysis']['60_days']:.2f}",
                f"- 90 Days: ${data['aging_analysis']['90_days']:.2f}",
                f"- 90+ Days: ${data['aging_analysis']['90_plus_days']:.2f}"
            ])
        
        elif report['type'] == 'client_analysis':
            summary.extend([
                f"Total Active Clients: {data['total_active_clients']}",
                f"Average Client Spend: ${data['average_client_spend']:.2f}"
            ])
        
        elif report['type'] == 'service_metrics':
            top_services = data['top_services'][:3]  # Show top 3 services
            summary.extend([
                "Top Services by Revenue:",
                *[f"- {service[0]}: ${service[1]['total_revenue']:.2f}" for service in top_services]
            ])
        
        elif report['type'] == 'payment_trends':
            summary.extend([
                f"Average Payment Size: ${data['average_payment_size']:.2f}",
                "\nPayment Methods:",
                *[f"- {method}: ${amount:.2f}" for method, amount in data['payment_methods'].items()]
            ])
        
        return "\n".join(summary) 