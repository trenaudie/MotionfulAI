# app.py
from flask import Flask, request, jsonify, current_app
from flask_cors import CORS  # <- Add this
import os
import yaml
from datetime import datetime
# load config from .env or similar
from paths import AGENTS_PROMPTS_DIR, SCENES_DIR
from agents.agents import CoderGeneralAgent

app = Flask(__name__)
CORS(app)  # <- Allow all origins by default

print(f"SCENES_DIR: {SCENES_DIR}")
print(f"AGENTS_PROMPTS_DIR: {AGENTS_PROMPTS_DIR}")
os.makedirs(SCENES_DIR, exist_ok=True)


def run_code_generation(prompt, dummy : bool = False):

    coder_general_agent = CoderGeneralAgent()
    filepath, status = coder_general_agent.generate_code(prompt)
    if status == 'success':
        return filepath
    else:
        raise Exception(f"Failed to generate code: {status}")


@app.route('/write_code', methods=['POST'])
def write_code_to_files():
    data = request.json or {}
    prompt = data.get('prompt')
    if not prompt:
        return jsonify({'error': 'Missing prompt'}), 400

    filename = run_code_generation(prompt)
    print(f'Scene2d written to {SCENES_DIR / filename}')
    return jsonify({'filename': filename}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)