import os
import logging
from flask import Flask, render_template, jsonify
from dotenv import load_dotenv
import json
import datetime

# Load environment variables from .env file
load_dotenv()

# Configuration class
class Config:
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    ACOUSTIC_FOLDER = os.path.join(BASE_DIR, 'static', 'acoustic')
    BEATS_FOLDER = os.path.join(BASE_DIR, 'static', 'beats')
    DEMO_FOLDER = os.path.join(BASE_DIR, 'static', 'demos')
    LIVE_FOLDER = os.path.join(BASE_DIR, 'static', 'live')  # Add the live folder
    ALLOWED_EXTENSIONS = {'wav', 'mp3', 'ogg'}
    VISITOR_FILE = 'visitor_count.json'

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

# Function to get the current visitor count from the visitor_count.json file
def get_visitor_count():
    try:
        if os.path.exists(app.config['VISITOR_FILE']):
            with open(app.config['VISITOR_FILE'], 'r') as f:
                data = json.load(f)
            return data.get('count', 0)
        return 0
    except Exception as e:
        logger.error(f"Error reading visitor count: {str(e)}")
        return 0

# Function to get a preview of the audio files
def get_audio_files_from_folder(folder_path, limit=2):
    audio_files_info = []
    if os.path.exists(folder_path):
        files = [f for f in os.listdir(folder_path) if f.endswith(tuple(app.config['ALLOWED_EXTENSIONS']))]
        for filename in files[:limit]:
            audio_files_info.append({
                'name': filename,
                'url': f'/static/{os.path.basename(folder_path)}/{filename}',
                'download_url': f'/static/{os.path.basename(folder_path)}/{filename}',
                'created_time': '2025-01-01',  # Optional: date of creation
            })
    return audio_files_info

# Routes
@app.route('/')
def home():
    increment_visitor_count()
    acoustic_files_info = get_audio_files_from_folder(app.config['ACOUSTIC_FOLDER'])
    beats_files_info = get_audio_files_from_folder(app.config['BEATS_FOLDER'])
    demo_files_info = get_audio_files_from_folder(app.config['DEMO_FOLDER'])
    return render_template('index.html', acoustic_files_info=acoustic_files_info,
                           beats_files_info=beats_files_info, demo_files_info=demo_files_info,
                           visitor_count=get_visitor_count())

@app.route('/portfolio')
def portfolio():
    try:
        acoustic_files_info = get_audio_files_from_folder(app.config['ACOUSTIC_FOLDER'], limit=None)
        beats_files_info = get_audio_files_from_folder(app.config['BEATS_FOLDER'], limit=None)
        demo_files_info = get_audio_files_from_folder(app.config['DEMO_FOLDER'], limit=None)
        live_files_info = get_audio_files_from_folder(app.config['LIVE_FOLDER'], limit=None)  # Fetch live files
        return render_template('portfolio.html', acoustic_files_info=acoustic_files_info,
                               beats_files_info=beats_files_info, demo_files_info=demo_files_info,
                               live_files_info=live_files_info)  # Pass live files to the template
    except Exception as e:
        logger.error(f"Error fetching files from folders: {str(e)}")
        return render_template('portfolio.html', error="Failed to retrieve audio files")

@app.route('/store')
def store():
    return render_template('store.html')

# Helper function to increment visitor count
def increment_visitor_count():
    try:
        visitor_count = get_visitor_count() + 1
        with open(app.config['VISITOR_FILE'], 'w') as f:
            json.dump({'count': visitor_count}, f)
    except Exception as e:
        logger.error(f"Error incrementing visitor count: {str(e)}")

if __name__ == '__main__':
    # Enable debug mode for local development
    app.run(debug=True, host='127.0.0.1', port=5000)
