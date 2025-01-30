from typing import List
from langchain.agents import AgentExecutor, AgentType, initialize_agent
from langchain.tools import tool
from base_agent import BaseAgent
import math

class TestAgent(BaseAgent):
    """A test agent that can perform basic calculations and answer questions."""
    
    def __init__(self, name: str = "TestAgent"):
        system_message = """You are a helpful assistant that can perform calculations and answer questions.
        You have access to Python's math capabilities and can perform complex calculations.
        Always show your work when doing calculations and explain your thinking process.
        """
        
        # Initialize tools
        @tool
        def calculate(expression: str) -> str:
            """Evaluates a mathematical expression. Input should be a valid Python math expression."""
            try:
                # Add math functions to the local namespace
                local_dict = {"math": math}
                result = eval(expression, {"__builtins__": {}}, local_dict)
                return f"Result: {result}"
            except Exception as e:
                return f"Error evaluating expression: {str(e)}"
        
        tools = [calculate]
        
        super().__init__(
            name=name,
            system_message=system_message,
            tools=tools,
            temperature=0.3  # Lower temperature for more precise responses
        )
    
    def initialize_agent(self) -> AgentExecutor:
        """Initialize the agent with tools and configuration."""
        return initialize_agent(
            tools=self.tools,
            llm=self.llm,
            agent=AgentType.CHAT_CONVERSATIONAL_REACT_DESCRIPTION,
            memory=self.memory,
            agent_kwargs=self.agent_kwargs,
            verbose=True
        )

if __name__ == "__main__":
    # Create and test the agent
    agent = TestAgent()
    
    # Test cases
    test_queries = [
        "What is the square root of 144?",
        "If I have 3 apples and multiply them by 4, how many do I have?",
        "Calculate the area of a circle with radius 5 units.",
        "What is 15% of 200?",
    ]
    
    print("Running test queries...")
    for query in test_queries:
        print(f"\nQuery: {query}")
        try:
            response = agent.run(query)
            print(f"Response: {response}")
        except Exception as e:
            print(f"Error: {str(e)}") 