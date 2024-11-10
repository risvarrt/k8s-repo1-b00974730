from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

@app.route('/calculate', methods=['POST'])
def calculate():
    data = request.get_json()

    # Validate input JSON
    if 'file' not in data or not data['file']:
        return jsonify({"file": None, "error": "Invalid JSON input."}), 400

    file_name = data['file']
    product = data.get('product', '')

    # Check if file exists locally
    filepath = os.path.join('/risvarrt_PV_dir', file_name)
    if not os.path.isfile(filepath):
        return jsonify({"file": file_name, "error": "File not found."}), 404

    # Forward the request to Container 2 and handle communication errors
    try:
        response = requests.post('http://ks-service2-b00974730:7002/process', json={"file": file_name, "product": product})
        response.raise_for_status()  # Raise an error if the response is unsuccessful
        return jsonify(response.json())
    except requests.exceptions.RequestException as e:
        return jsonify({"file": file_name, "error": "Error communicating with Container 2.", "details": str(e)}), 502

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002)
