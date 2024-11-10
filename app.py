from flask import Flask, request, jsonify
import requests
import os
import csv

app = Flask(__name__)
# test
@app.route('/calculate', methods=['POST'])
def calculate():
    data = request.get_json() 

    # Validate input JSON
    if 'file' not in data or not data['file']:
        return jsonify({"file": None, "error": "Invalid JSON input."}), 400

    file_name = data['file']
    product = data.get('product', '')
    
    filepath = os.path.join('/risvarrt_PV_dir', file_name)
    
    # Check if the file exists
    if not os.path.isfile(filepath):
        return jsonify({"file": file_name, "error": "File not found."}), 404
    
    # Forward the request to Container 2
    response = requests.post('http://ks-service2-b00974730:7002/calculate', json={"file": file_name, "product": product})
    return jsonify(response.json())

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002)
