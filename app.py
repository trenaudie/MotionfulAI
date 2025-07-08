# app.py
from flask import Flask, request, jsonify, current_app
from flask_cors import CORS  # <- Add this
import os
import yaml
from datetime import datetime
from dotenv import load_dotenv
load_dotenv()  # Load environment variables from .env
# load config from .env or similar
from paths import AGENTS_PROMPTS_DIR, SCENES_DIR, get_next_scene_filepath
from agents.coder_general_agent import CoderGeneralAgent

app = Flask(__name__)
CORS(app)  # <- Allow all origins by default

print(f"SCENES_DIR: {SCENES_DIR}")
print(f"AGENTS_PROMPTS_DIR: {AGENTS_PROMPTS_DIR}")
os.makedirs(SCENES_DIR, exist_ok=True)


def run_code_generation(prompt, dummy : bool = False):
    if dummy: return "dummy.tsx", "success"
    coder_general_agent = CoderGeneralAgent()
    filepath, status = coder_general_agent.generate_code(prompt)
    if status == 'success':
        return filepath
    code_v1, reasoning_v1 = coder_general_agent.generate_code(prompt)
    print(f'code_v1: {code_v1}')
    print(f'reasoning_v1: {reasoning_v1}')
    filepath_return = get_next_scene_filepath()
    return filepath_return


@app.route('/write_code', methods=['POST'])
def write_code_to_files():
    print(f'POST - WRITING CODE TO FILES')
    data = request.json or {}
    prompt = data.get('prompt')
    if not prompt:
        return jsonify({'error': 'Missing prompt'}), 400

    filename = run_code_generation(prompt)
    print(f'Scene2d written to {SCENES_DIR / filename}')
    return jsonify({'filename': str(filename)}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)