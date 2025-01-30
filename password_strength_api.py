from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import pickle
import string

app = Flask(__name__)
CORS(app)

# Load the trained model
with open("password_strength_model.pkl", "rb") as model_file:
    model = pickle.load(model_file)

# Serve the HTML file
@app.route('/')
def serve_index():
    return send_from_directory('.', 'index.html')

# Prediction endpoint
@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json()
    password = data.get('password', '')
    if not password:
        return jsonify({"error": "Password is required."}), 400

    features = {
        'length': len(password),
        'num_uppercase': sum(1 for c in password if c.isupper()),
        'num_lowercase': sum(1 for c in password if c.islower()),
        'num_digits': sum(1 for c in password if c.isdigit()),
        'num_special': sum(1 for c in password if c in string.punctuation),
    }
    features_df = [list(features.values())]
    prediction = model.predict(features_df)[0]
    prediction_label = {0: 'Weak', 1: 'Moderate', 2: 'Strong'}[prediction]

    return jsonify({"password": password, "strength": prediction_label})

if __name__ == '__main__':
    app.run(debug=True)
