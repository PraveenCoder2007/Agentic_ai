# LangChain Multi-Agent Routing System

A simple agent-like system using LangChain and Google's Generative AI that demonstrates routing user requests to different specialized handlers based on intent classification.

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Set up your Google API key:
```bash
# Copy the example environment file
copy .env.example .env

# Edit .env and add your actual Google API key
GOOGLE_API_KEY=your_actual_api_key_here
```

## Usage

Run the example:
```bash
python langchain_routing.py
```

## How It Works

The system consists of:
- **Coordinator Router**: Uses LLM to classify requests as 'booker', 'info', or 'unclear'
- **Sub-Agent Handlers**: Specialized functions for different request types
- **Delegation Logic**: Routes requests to appropriate handlers based on classification

## Example Requests

- Booking: "Book me a flight to London"
- Information: "What is the capital of Italy?"
- Unclear: "Tell me about quantum physics"