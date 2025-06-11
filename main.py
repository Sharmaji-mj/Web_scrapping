from flask import Flask, jsonify
import extract 

app = Flask(__name__)

@app.route('/run', methods=['GET'])
def run_script():
    data = extract.py.run() 
    return jsonify(data)

if __name__ == '__main__':
    app.run()

