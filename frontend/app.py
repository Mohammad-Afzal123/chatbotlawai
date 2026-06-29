import os
import requests
import logging
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import ollama

app = Flask(__name__, static_folder='.', static_url_path='')
CORS(app)

@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

API_TOKEN = os.environ.get("INDIAN_KANOON_API_TOKEN", "e35e88529791d1e5f6c7a6a34fe15a16c1198b24")
SEARCH_URL = "https://api.indiankanoon.org/search/"

OLLAMA_MODEL = os.environ.get("OLLAMA_MODEL", "llama3.2")
OLLAMA_URL = os.environ.get("OLLAMA_URL", "http://localhost:11434")

def query_ollama(prompt):
    try:
        response = ollama.generate(
            model=OLLAMA_MODEL,
            prompt=prompt,
            stream=False
        )
        return response['response']
    except Exception as e:
        logger.error(f"Ollama query failed: {e}")
        raise

@app.route('/search', methods=['GET'])
def search():
    query = request.args.get('q')
    if not query:
        return jsonify({"error": "Missing query parameter"}), 400

    headers = {
        "Authorization": f"Token {API_TOKEN}"
    }

    payload = {
        "formInput": query
    }

    logger.info(f"Trying Indian Kanoon for: '{query}'")

    try:
        response = requests.post(SEARCH_URL, data=payload, headers=headers, timeout=10)
        response.raise_for_status()
        kanoon_data = response.json()

        if not kanoon_data or 'error' in kanoon_data or (isinstance(kanoon_data, list) and len(kanoon_data) == 0):
            raise ValueError("Indian Kanoon returned no useful results")

        logger.info("Indian Kanoon returned results. Forwarding to Ollama for analysis.")

        prompt = (
            "Please analyze the following legal information and provide a summary of the key points, relevant laws mentioned, and the outcome if available:\n\n"
            f"{kanoon_data}\n\n"
            "Conclude with advice or next steps based on the text. Avoid special characters like *."
        )
        ollama_response = query_ollama(prompt)
        return jsonify({"source": "Indian Kanoon", "analysis": ollama_response})

    except Exception as e:
        logger.warning(f"Indian Kanoon failed. Falling back to Ollama. Reason: {e}")
        prompt = (
            f"The user asked: \"{query}\".\n"
            "Please provide a legal explanation, relevant Indian laws if applicable, and advice."
        )
        try:
            ollama_response = query_ollama(prompt)
            return jsonify({"source": "Ollama (fallback)", "analysis": ollama_response})
        except Exception as gerr:
            logger.error(f"Ollama failed: {gerr}")
            return jsonify({"error": "Both Indian Kanoon and Ollama failed.", "details": str(gerr)}), 500

if __name__ == '__main__':
    port = int(os.environ.get("FLASK_PORT", 5000))
    app.run(debug=True, host='0.0.0.0', port=port)
