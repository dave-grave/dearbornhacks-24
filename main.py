from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/')
def index():
    return "Welcome to the AI Voice Assistant API"

@app.route('/test', methods=['GET'])
def test_endpoint():
    return jsonify({
        "message": "API is working!",
        "status": "success"
    })

@app.route('/echo/<message>', methods=['GET'])
def echo(message):
    return jsonify({
        "message": f"You said: {message}",
        "status": "success"
    })

if __name__ == '__main__':
    app.run(debug=True)