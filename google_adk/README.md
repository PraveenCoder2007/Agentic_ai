# Google Agent Developer Kit (ADK) Examples

This folder contains three examples demonstrating the Google ADK capabilities:

## Files

1. **google_search_agent.py** - Agent with Google Search tool integration
2. **code_execution_agent.py** - Agent with Python code execution capabilities  
3. **enterprise_search_agent.py** - Agent with Vertex AI Search integration

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Set up environment variables:
```bash
copy .env.example .env
# Edit .env and add your actual API keys
```

## Usage

Run individual examples:
```bash
python google_search_agent.py
python code_execution_agent.py
python enterprise_search_agent.py
```

## Requirements

- Google API Key
- For enterprise search: Vertex AI Search datastore ID
- Python 3.8+