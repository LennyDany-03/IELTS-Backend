import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Azure OpenAI for both essay and speech evaluation
AZURE_OPENAI_KEY = os.getenv("AZURE_OPENAI_KEY")
AZURE_OPENAI_ENDPOINT = os.getenv("AZURE_OPENAI_ENDPOINT")
AZURE_OPENAI_DEPLOYMENT_ID = os.getenv("AZURE_OPENAI_DEPLOYMENT_ID")
AZURE_OPENAI_API_VERSION = os.getenv("AZURE_OPENAI_API_VERSION")

# For essay evaluation (specific deployment name, if needed separately)
AZURE_DEPLOYMENT = os.getenv("AZURE_DEPLOYMENT")  # Optional alias if different from above

# Azure Speech service config
AZURE_SPEECH_KEY = os.getenv("AZURE_SPEECH_KEY")
AZURE_SPEECH_ENDPOINT = os.getenv("AZURE_SPEECH_ENDPOINT")
AZURE_SPEECH_DEPLOYMENT_ID = os.getenv("AZURE_SPEECH_DEPLOYMENT_ID")
AZURE_SPEECH_API_VERSION = os.getenv("AZURE_SPEECH_API_VERSION")
