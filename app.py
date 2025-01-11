from flask import Flask, render_template, request, jsonify
import os
import logging
from dotenv import load_dotenv
from convert import convert_audio  # Import the convert_audio function from convert.py

# Load environment variables from .env file
load_dotenv()

# Configuration class
class Config:
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    ACOUSTIC_FOLDER = os.path.join(BASE_DIR, 'static', 'acoustic')
    BEATS_FOLDER = os.path.join(BASE_DIR, 'static', 'beats')
    DEMO_FOLDER = os.path.join(BASE_DIR, 'static', 'demos')
    LIVE_FOLDER = os.path.join(BASE_DIR, 'static', 'live')
    SONGS_FOLDER = os.path.join(BASE_DIR, 'static', 'songs')  # Add the songs folder
    ALLOWED_EXTENSIONS = {'wav', 'mp3', 'ogg'}
    VISITOR_FILE = os.path.join(BASE_DIR, 'visitor_count.json')

    FLASK_ENV = os.getenv('FLASK_ENV', 'production')  # Default to production if not set
    SECRET_KEY = os.getenv('SECRET_KEY', 'your-secret-key')  # Should be set to a strong key in production

app = Flask(__name__)
app.config.from_object(Config)

# Initialize logging
logging.basicConfig(
    level=logging.DEBUG if os.getenv('FLASK_ENV') == 'development' else logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('app.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Create required directories if they don't exist
os.makedirs(app.config['ACOUSTIC_FOLDER'], exist_ok=True)
os.makedirs(app.config['BEATS_FOLDER'], exist_ok=True)
os.makedirs(app.config['DEMO_FOLDER'], exist_ok=True)
os.makedirs(app.config['LIVE_FOLDER'], exist_ok=True)
os.makedirs(app.config['SONGS_FOLDER'], exist_ok=True)  # Create the songs folder

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/convert')
def convert_page():
    return render_template('convert.html')

@app.route('/convert', methods=['POST'])
def convert():
    return convert_audio()  # Just call convert_audio directly, Flask handles the request object

if __name__ == '__main__':
    app.run(debug=True, port=5001)  # Use port 5001 to avoid conflict with default Flask port
