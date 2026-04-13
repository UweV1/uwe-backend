from flask import Flask, request, Response, jsonify
from flask_cors import CORS
import requests

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

@app.route('/')
def index():
    return 'Uwe Backend läuft! 🎉'

@app.route('/speak', methods=['POST', 'OPTIONS'])
def speak():
    if request.method == 'OPTIONS':
        response = Response()
        response.headers['Access-Control-Allow-Origin'] = '*'
        response.headers['Access-Control-Allow-Methods'] = 'POST, OPTIONS'
        response.headers['Access-Control-Allow-Headers'] = 'Content-Type'
        return response

    data = request.json or {}
    text     = data.get('text', '')
    el_key   = data.get('el_key', '')
    voice_id = data.get('voice_id', 'H2QCuT74DBr1ntvAhQss')

    if not text or not el_key:
        return jsonify({'error': 'text und el_key erforderlich'}), 400

    url = f'https://api.elevenlabs.io/v1/text-to-speech/{voice_id}'
    headers = {
        'xi-api-key': el_key,
        'Content-Type': 'application/json',
        'Accept': 'audio/mpeg'
    }
    body = {
        'text': text,
        'model_id': 'eleven_multilingual_v2',
        'voice_settings': {
            'stability': 0.4,
            'similarity_boost': 0.75,
            'style': 0.6,
            'use_speaker_boost': True
        }
    }

    r = requests.post(url, json=body, headers=headers)

    if not r.ok:
        return jsonify({'error': f'ElevenLabs Fehler: {r.status_code}', 'detail': r.text}), r.status_code

    response = Response(r.content, mimetype='audio/mpeg')
    response.headers['Access-Control-Allow-Origin'] = '*'
    return response

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
