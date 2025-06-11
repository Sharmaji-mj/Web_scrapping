from flask import Flask, send_file
import subprocess
import os

app = Flask(__name__)

@app.route('/run-script', methods=['GET'])
def run_script():
    try:
        # Run your script (make sure it generates `tender.csv`)
        subprocess.run(['python3', 'WEB SCRAPPING/extract.py'], check=True)
        
        # Return the CSV file
        file_path = 'WEB SCRAPPING/tender.csv'
        if os.path.exists(file_path):
            return send_file(file_path, mimetype='text/csv', as_attachment=True)
        else:
            return {"error": "CSV not found"}, 404

    except subprocess.CalledProcessError as e:
        return {"error": f"Script failed: {str(e)}"}, 500

if __name__ == '__main__':
    app.run(debug=True)
