import google.generativeai as genai
import os
import logging
from flask import Flask, request, jsonify, Response # Added Response
from flask_cors import CORS


logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app) 

API_KEY = os.environ.get("GOOGLE_API_KEY")
model = None 

if not API_KEY:

    API_KEY = "AIzaSyCqBPd9TySmHHbqXHB_QMPbH7SbM920flc" 
    logger.warning(
        "GOOGLE_API_KEY environment variable not set. Using a default/placeholder key from the script. "
        "For this to work, ensure this key is valid or set the GOOGLE_API_KEY environment variable."
    )
else:
    logger.info("GOOGLE_API_KEY loaded from environment variable.")

try:
    genai.configure(api_key=API_KEY)
    MODEL_NAME = os.environ.get("GEMINI_MODEL_NAME", "gemini-1.5-flash")
    model = genai.GenerativeModel(model_name=MODEL_NAME)
    logger.info(f"Successfully configured Gemini AI with model: {MODEL_NAME}")
except Exception as e:
    logger.error(f"Failed to configure Gemini AI or initialize model: {e}. The /generate endpoint will not work.")

@app.route('/ask_gemini', methods=['POST']) 
def ask_gemini_endpoint(): 
    if not model:
        logger.error("Gemini model is not initialized. Cannot process request.")
        return jsonify({"error": "Gemini model not initialized. Check server logs."}), 500

    data = request.get_json()
    if not data or 'prompt' not in data:
        logger.warning("Request to /ask_gemini received without 'prompt' in JSON body.")
        return jsonify({"error": "Missing 'prompt' in request body"}), 400

    prompt = data['prompt']
    logger.info(f"Received prompt for /ask_gemini: '{prompt[:100]}{'...' if len(prompt) > 100 else ''}'")

    try:
        gemini_response_obj = model.generate_content(prompt) 
        logger.info("Successfully generated content from Gemini.")
        return Response(gemini_response_obj.text, mimetype='text/plain')
    except Exception as e:
        logger.error(f"Error during Gemini content generation: {e}")
        return jsonify({"error": "Failed to generate content from Gemini", "details": str(e)}), 500

if __name__ == "__main__":
    port = int(os.environ.get("GEMINI_PORT", 5001))
    logger.info(f"Starting Gemini backend server on http://0.0.0.0:{port}")
    app.run(debug=True, host='0.0.0.0', port=port)
