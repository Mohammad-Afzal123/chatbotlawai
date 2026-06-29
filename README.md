# Indian Kanoon Legal Chatbot

A simple chatbot that uses Indian Kanoon API for legal data and Ollama (local LLM) for analysis.

## Features
- Fetches legal data from Indian Kanoon API
- Analyzes data using locally running Ollama model
- Clean, simple web interface
- PDF download of results

## Prerequisites
1. Python 3.8 or higher
2. [Ollama](https://ollama.com/) installed on your machine

## Setup Instructions

### 1. Clone or download this repository
```bash
git clone <repository-url>
cd chatbotlawai
```

### 2. Install Python dependencies
```bash
pip install -r requirements.txt
```

### 3. Set up Ollama
#### a. Start Ollama server
```bash
ollama serve
```
Or start it via the Ollama desktop app (recommended for easier use).

#### b. Pull your desired model (e.g., llama3.2)
```bash
ollama pull llama3.2
```
You can use any Ollama model you prefer - just update the `OLLAMA_MODEL` environment variable or in `frontend/app.py`.

### 4. Run the backend server
```bash
cd frontend
python app.py
```

### 5. Open the web interface
Open `frontend/index.html` in your browser.

## Environment Variables (Optional)
You can configure these if needed:
- `INDIAN_KANOON_API_TOKEN`: Your Indian Kanoon API token (default is provided)
- `OLLAMA_MODEL`: Name of the Ollama model to use (default: `llama3.2`)
- `OLLAMA_URL`: URL of your Ollama server (default: `http://localhost:11434`)
- `FLASK_PORT`: Port for Flask server (default: `5000`)

## Usage
1. Type your legal query in the search box
2. Click "Search"
3. Wait for the analysis from Ollama
4. (Optional) Click "Download PDF" to save the results
