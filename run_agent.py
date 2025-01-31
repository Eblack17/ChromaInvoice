from billing_agent import BillingAgent

def main():
    print("Starting ChromaInvoice Billing Agent...")
    agent = BillingAgent()
    agent_executor = agent.initialize_agent()
    
    print("\nBilling Agent is ready! You can:")
    print("1. Generate invoices")
    print("2. Track invoice status")
    print("3. Send payment reminders")
    print("4. Record payments")
    print("5. Generate financial reports")
    print("\nType 'exit' to quit")
    
    while True:
        try:
            print("\nWhat would you like to do?")
            query = input("> ")
            
            if query.lower() == 'exit':
                print("Goodbye!")
                break
            
            if query.strip():
                response = agent_executor.invoke({"input": query})
                print("\nResponse:", response["output"])
                
        except KeyboardInterrupt:
            print("\nGoodbye!")
            break
        except Exception as e:
            print(f"\nError: {str(e)}")

if __name__ == "__main__":
    main() 