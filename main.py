from flask import Flask, request, jsonify
app = Flask(__name__)

@app.route('/')
def index():
    return "<h1>SIAP</h1>"

if __name__ == '__main__':
    # Threaded option to enable multiple instances for multiple user access support
    print("Init app in port 5000")
    app.run(port=5000, debug=True)