from typing import List, Dict, Any
from langchain.agents import AgentExecutor, AgentType, initialize_agent
from langchain.tools import tool
from base_agent import BaseAgent
from database import BillingDatabase
from datetime import datetime, timedelta
import json
import math
import re

class BillingAgent(BaseAgent):
    """AI Billing Assistant Agent for Chromapages"""
    
    def __init__(self, name: str = "BillingAssistant"):
        system_message = """You are an AI Billing Assistant for Chromapages, a web design and services business.
        Your responsibilities include:
        - Generating and managing invoices
        - Sending payment reminders
        - Processing payments
        - Managing financial records
        - Providing financial insights and reports
        
        Always be professional, accurate, and maintain confidentiality with financial information.
        Explain your actions clearly and provide detailed responses when handling financial matters.
        
        When handling JSON data:
        1. Always validate the data structure before processing
        2. Ensure all required fields are present
        3. Format currency values as numbers without the $ symbol
        4. Use ISO format for dates or specify days for relative dates
        """
        
        # Initialize database
        self.db = BillingDatabase()
        
        # Initialize tools
        tools = [
            self._create_invoice_tool(),
            self._track_invoice_tool(),
            self._payment_reminder_tool(),
            self._generate_report_tool(),
            self._record_payment_tool()
        ]
        
        super().__init__(
            name=name,
            system_message=system_message,
            tools=tools,
            temperature=0.2  # Lower temperature for higher precision in financial matters
        )
    
    def _parse_amount(self, amount_str: str) -> float:
        """Parse amount string to float, removing currency symbols"""
        if isinstance(amount_str, (int, float)):
            return float(amount_str)
        return float(re.sub(r'[^\d.]', '', amount_str))
    
    def _create_invoice_tool(self):
        @tool
        def generate_invoice(invoice_data: str) -> str:
            """
            Generates an invoice based on provided data.
            Input should be a JSON string with: client_name, services (list), amount, due_date
            Example: {"client_name": "TechCorp", "services": ["Web Design"], "amount": 2000, "due_date": 30}
            """
            try:
                if isinstance(invoice_data, str):
                    data = json.loads(invoice_data)
                else:
                    data = invoice_data
                
                # Validate required fields
                required_fields = ["client_name", "services", "amount"]
                missing_fields = [field for field in required_fields if field not in data]
                if missing_fields:
                    return f"Error: Missing required fields: {', '.join(missing_fields)}"
                
                # Parse amount
                data['amount'] = self._parse_amount(data['amount'])
                
                # Handle due date
                if 'due_date' not in data:
                    data['due_date'] = (datetime.now() + timedelta(days=30)).isoformat()
                elif isinstance(data['due_date'], int):
                    data['due_date'] = (datetime.now() + timedelta(days=data['due_date'])).isoformat()
                
                # Create invoice in database
                invoice_id = self.db.create_invoice(data)
                return f"Invoice {invoice_id} generated for {data['client_name']} for services: {', '.join(data['services'])}. Amount: ${data['amount']:.2f}, Due: {data['due_date']}"
            except Exception as e:
                return f"Error generating invoice: {str(e)}"
        return generate_invoice
    
    def _track_invoice_tool(self):
        @tool
        def track_invoice(invoice_id: str) -> str:
            """
            Tracks the status of an invoice by ID.
            Example: "INV-20240301-123456"
            """
            try:
                invoice = self.db.get_invoice(invoice_id)
                if invoice:
                    due_date = datetime.fromisoformat(invoice['due_date'])
                    days_until_due = (due_date - datetime.now()).days
                    status_info = f"({days_until_due} days until due)" if days_until_due > 0 else "(OVERDUE)"
                    
                    return (f"Invoice {invoice_id}:\n"
                           f"Status: {invoice['status']} {status_info}\n"
                           f"Client: {invoice['client_name']}\n"
                           f"Amount: ${invoice['amount']:.2f}\n"
                           f"Due Date: {invoice['due_date']}")
                return f"Invoice {invoice_id} not found"
            except Exception as e:
                return f"Error tracking invoice: {str(e)}"
        return track_invoice
    
    def _payment_reminder_tool(self):
        @tool
        def send_reminder(invoice_data: str) -> str:
            """
            Sends payment reminder for overdue invoices.
            Input should be a JSON string with: invoice_id
            Example: {"invoice_id": "INV-20240301-123456"}
            """
            try:
                if isinstance(invoice_data, str):
                    data = json.loads(invoice_data)
                else:
                    data = invoice_data
                
                invoice_id = data['invoice_id']
                invoice = self.db.get_invoice(invoice_id)
                
                if not invoice:
                    return f"Invoice {invoice_id} not found"
                
                if invoice['status'] == 'paid':
                    return f"Invoice {invoice_id} has already been paid"
                
                due_date = datetime.fromisoformat(invoice['due_date'])
                days_overdue = (datetime.now() - due_date).days
                
                # Update invoice status and send reminder
                self.db.update_invoice_status(invoice_id, "reminder_sent")
                return (f"Payment reminder sent for invoice {invoice_id} to {invoice['client_name']}\n"
                       f"Amount Due: ${invoice['amount']:.2f}\n"
                       f"Days Overdue: {days_overdue if days_overdue > 0 else 0}")
            except Exception as e:
                return f"Error sending reminder: {str(e)}"
        return send_reminder
    
    def _record_payment_tool(self):
        @tool
        def record_payment(payment_data: str) -> str:
            """
            Records a payment for an invoice.
            Input should be a JSON string with: invoice_id, amount, payment_method
            Example: {"invoice_id": "INV-20240301-123456", "amount": 2000, "payment_method": "Credit Card"}
            """
            try:
                if isinstance(payment_data, str):
                    data = json.loads(payment_data)
                else:
                    data = payment_data
                
                # Validate required fields
                required_fields = ["invoice_id", "amount", "payment_method"]
                missing_fields = [field for field in required_fields if field not in data]
                if missing_fields:
                    return f"Error: Missing required fields: {', '.join(missing_fields)}"
                
                # Parse amount
                data['amount'] = self._parse_amount(data['amount'])
                
                # Record payment
                payment_id = self.db.record_payment(data)
                return f"Payment {payment_id} recorded for invoice {data['invoice_id']}. Amount: ${data['amount']:.2f}"
            except Exception as e:
                return f"Error recording payment: {str(e)}"
        return record_payment
    
    def _generate_report_tool(self):
        @tool
        def generate_financial_report(report_params: str) -> str:
            """
            Generates financial reports.
            Input should be a JSON string with: report_type, start_date (optional), end_date (optional)
            Report types: revenue, outstanding, trends
            Example: {"report_type": "revenue", "start_date": "2024-03-01", "end_date": "2024-03-31"}
            """
            try:
                if isinstance(report_params, str):
                    params = json.loads(report_params)
                else:
                    params = report_params
                
                if 'report_type' not in params:
                    return "Error: report_type is required"
                
                # Set default date range if not provided
                if 'start_date' not in params:
                    params['start_date'] = datetime.now().replace(day=1).isoformat()
                if 'end_date' not in params:
                    params['end_date'] = datetime.now().isoformat()
                
                # Convert string dates to datetime
                start_date = datetime.fromisoformat(params['start_date'])
                end_date = datetime.fromisoformat(params['end_date'])
                
                report = self.db.generate_report(params['report_type'], start_date, end_date)
                return f"Generated {params['report_type']} report:\n{json.dumps(report, indent=2)}"
            except Exception as e:
                return f"Error generating report: {str(e)}"
        return generate_financial_report
    
    def initialize_agent(self) -> AgentExecutor:
        """Initialize the billing agent with tools and configuration."""
        return initialize_agent(
            tools=self.tools,
            llm=self.llm,
            agent=AgentType.STRUCTURED_CHAT_ZERO_SHOT_REACT_DESCRIPTION,
            memory=self.memory,
            agent_kwargs=self.agent_kwargs,
            verbose=True
        )

if __name__ == "__main__":
    # Create the billing agent
    agent = BillingAgent() 