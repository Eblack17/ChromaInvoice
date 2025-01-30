from typing import List, Optional, Union
from langchain.agents import AgentExecutor
from langchain.schema import AgentAction, AgentFinish
from langchain.memory import ConversationBufferMemory
from langchain.prompts import MessagesPlaceholder
from langchain_google_genai import ChatGoogleGenerativeAI
import google.generativeai as genai
from config import GOOGLE_API_KEY, DEFAULT_MODEL, TEMPERATURE, MAX_TOKENS

# Configure Google Generative AI
genai.configure(api_key=GOOGLE_API_KEY)

class BaseAgent:
    def __init__(
        self,
        name: str,
        system_message: str,
        tools: List = None,
        model: str = DEFAULT_MODEL,
        temperature: float = TEMPERATURE,
        max_tokens: int = MAX_TOKENS,
        memory: Optional[ConversationBufferMemory] = None
    ):
        self.name = name
        self.system_message = system_message
        self.tools = tools or []
        
        # Initialize memory with the latest structure
        self.memory = memory or ConversationBufferMemory(
            return_messages=True,
            memory_key="chat_history",
            output_key="output"
        )
        
        # Initialize the language model
        self.llm = ChatGoogleGenerativeAI(
            model=model,
            temperature=temperature,
            max_output_tokens=max_tokens,
            google_api_key=GOOGLE_API_KEY,
            convert_system_message_to_human=True
        )
        
        # Initialize agent components
        self.agent_kwargs = {
            "system_message": system_message,
            "extra_prompt_messages": [MessagesPlaceholder(variable_name="chat_history")]
        }
        
    def initialize_agent(self) -> AgentExecutor:
        """Initialize the agent executor with the current configuration"""
        raise NotImplementedError("Subclasses must implement initialize_agent()")
        
    def run(self, input_text: str) -> Union[AgentAction, AgentFinish]:
        """Run the agent with the given input"""
        agent_executor = self.initialize_agent()
        return agent_executor.invoke({"input": input_text})["output"]
        
    def add_tool(self, tool) -> None:
        """Add a new tool to the agent's toolkit"""
        self.tools.append(tool)
        
    def remove_tool(self, tool_name: str) -> None:
        """Remove a tool from the agent's toolkit by name"""
        self.tools = [t for t in self.tools if t.name != tool_name] 