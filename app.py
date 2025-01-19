from flask import Flask, jsonify
import secrets_confiq
from utils.customJSONEncoder import CustomJSONProvider
from services.phones import phones
# from services.firebase_auth import firebase_mock_service
from services.users import users
from services.files import files
from flask_cors import CORS

app = Flask(__name__)
app.json = CustomJSONProvider(app)
secrets_confiq.run_secrets_configurations()
CORS(app, resources={r"/*": {"origins": ["http://localhost:3000", "http://10.0.29.185:7070", "https://www.phonebuddy.store"]}})

# Services
app.register_blueprint(phones, url_prefix="/phones")
app.register_blueprint(users, url_prefix="/users")
app.register_blueprint(files, url_prefix="/files")
# app.register_blueprint(firebase_mock_service, url_prefix="/f")


@app.route('/', methods=['GET'])
def index():
    return jsonify("Phone Buddy API V1")

@app.route('/health', methods=['GET'])
def health():
    return jsonify("Phone Buddy API is healthy")


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=7070, debug=True)