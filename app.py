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
CORS(app, resources={r"/*": {"origins": ["http://localhost:3000", "http://10.0.29.185:7070"]}})

# Services
app.register_blueprint(phones, url_prefix="/phones")
app.register_blueprint(users, url_prefix="/users")
app.register_blueprint(files, url_prefix="/files")
# app.register_blueprint(firebase_mock_service, url_prefix="/f")


@app.route('/', methods=['GET'])
def index():
    return jsonify("Inventory Tracker API V2024.04.02")


# if __name__ == '__main__':
#     app.run(host='0.0.0.0', port=7070, debug=True)

from flask_lambda import FlaskLambda
app = FlaskLambda(app)
