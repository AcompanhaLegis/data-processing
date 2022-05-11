from flask import Flask
from flask_cors import CORS

PORT = 9000
DATA_DIR = "./deputados_data_digest"

# Initialize
app = Flask('acompanha-legis-data', static_url_path='/', static_folder=DATA_DIR, )
cors = CORS(app, resources={r"/*": {"origins": "*"}})

app.run(host='0.0.0.0', port=PORT, debug=True)