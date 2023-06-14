import json
import os
from functools import wraps
from pathlib import Path

from dotenv import load_dotenv
from flask import Flask, jsonify, request

from text_to_speech import go_ssml

app = Flask(__name__)
load_dotenv()

SERVER_KEY = os.getenv("API_KEY")


def require_api_key(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        api_key = request.headers.get('X-API-Key')

        if api_key is None:
            api_key = request.args.get('api_key')

        if api_key is None:
            return jsonify({'message': 'Please provide API Key'}), 401

        if api_key != SERVER_KEY:
            return jsonify({'message': 'Invalid API key'}), 401

        return func(*args, **kwargs)

    return decorated_function


@app.post('/api/synthesize')
@require_api_key
def synthesize():
    data = json.loads(request.data)
    path = Path(f"speech/{data['title']}")
    response = go_ssml(path, data["ssml"])
    return jsonify({'audio_file_path': str(response)})


if __name__ == '__main__':
    app.run(debug=True, host="127.0.0.1", port=8001)
