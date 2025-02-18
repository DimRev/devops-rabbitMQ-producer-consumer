import datetime
from flask import Flask, request

app = Flask(__name__)

@app.route('/healthz')
def healthz():
    return 'OK!'

@app.route('/msg', methods=['POST'])
def print_route():
    body = request.get_json()
    if "message" not in body:
        return "Message not found", 400
    print(f"{datetime.datetime.now()}: Received message: {body['message']}")
    return "Message received", 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)