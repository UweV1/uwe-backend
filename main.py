from flask import Flask, request, Response
from flask_cors import CORS
import requests

app = Flask(__name__)
CORS(app)  # Erlaubt Browser-Anfragen

@app.route('/speak', methods=['POST'])
def speak():
    data = request.json
    text     = data.get('text', '')
    el_key   = data.get('el_key', '')
    voice_id = data.get('voice_id', 'H2QCuT74DBr1ntvAhQss')

    if not text or not el_key:
        return {'error': 'text und el_key erforderlich'}, 400

    # Anfrage an ElevenLabs
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
        return {'error': f'ElevenLabs Fehler: {r.status_code}'}, r.status_code

    # Audio zurückschicken
    return Response(r.content, mimetype='audio/mpeg')

@app.route('/')
def index():
    return 'Uwe Backend läuft! 🎉'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
