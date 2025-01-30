from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# API Keys
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

# Model configurations
DEFAULT_MODEL = "gemini-pro"  # Gemini's base model
TEMPERATURE = 0.7
MAX_TOKENS = 1000  # Note: Gemini uses different token counting than OpenAI

# Agent configurations
AGENT_TIMEOUT = 60  # seconds
MAX_ITERATIONS = 3  # Maximum number of iterations for agent loops 