from flask import Flask, render_template, jsonify, request
import os
import logging
from dotenv import load_dotenv
import json

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

def get_audio_files_from_folder(folder_path, limit=None):
    audio_files_info = []
    if os.path.exists(folder_path):
        files = [f for f in os.listdir(folder_path) if f.endswith(tuple(app.config['ALLOWED_EXTENSIONS']))]
        logger.debug(f"Files found in {folder_path}: {files}")  # Log the found files

        if files:
            for filename in files[:limit]:
                audio_files_info.append({
                    'name': filename,
                    'url': f'/static/{os.path.basename(folder_path)}/{filename}',
                    'download_url': f'/static/{os.path.basename(folder_path)}/{filename}',
                    'created_time': '2025-01-01',
                })
        else:
            logger.debug(f"No valid audio files found in {folder_path}.")
    else:
        logger.error(f"Folder does not exist: {folder_path}")
    return audio_files_info

# Function to get visitor count
def get_visitor_count():
    if os.path.exists(app.config['VISITOR_FILE']):
        with open(app.config['VISITOR_FILE'], 'r') as f:
            data = json.load(f)
            return data.get('visitor_count', 0)
    return 0

# Function to increment visitor count
def increment_visitor_count():
    visitor_count = get_visitor_count() + 1
    with open(app.config['VISITOR_FILE'], 'w') as f:
        json.dump({'visitor_count': visitor_count}, f)

# Routes
@app.route('/')
def home():
    increment_visitor_count()
    acoustic_files_info = get_audio_files_from_folder(app.config['ACOUSTIC_FOLDER'])
    beats_files_info = get_audio_files_from_folder(app.config['BEATS_FOLDER'])
    demo_files_info = get_audio_files_from_folder(app.config['DEMO_FOLDER'])
    live_files_info = get_audio_files_from_folder(app.config['LIVE_FOLDER'])
    songs_info = get_audio_files_from_folder(app.config['SONGS_FOLDER'])  # Fetch songs

    logger.debug(f"Acoustic Files: {acoustic_files_info}")
    logger.debug(f"Beats Files: {beats_files_info}")
    logger.debug(f"Demo Files: {demo_files_info}")
    logger.debug(f"Live Files: {live_files_info}")
    logger.debug(f"Songs Info: {songs_info}")

    return render_template('index.html', 
                           acoustic_files_info=acoustic_files_info,
                           beats_files_info=beats_files_info, 
                           demo_files_info=demo_files_info,
                           live_files_info=live_files_info,
                           songs_info=songs_info,  # Pass songs_info to the template
                           visitor_count=get_visitor_count())

@app.route('/portfolio', methods=['GET'])
def portfolio():
    try:
        # Fetch the necessary data for the portfolio
        acoustic_files_info = get_audio_files_from_folder(app.config['ACOUSTIC_FOLDER'], limit=None)
        beats_files_info = get_audio_files_from_folder(app.config['BEATS_FOLDER'], limit=None)
        demo_files_info = get_audio_files_from_folder(app.config['DEMO_FOLDER'], limit=None)
        live_files_info = get_audio_files_from_folder(app.config['LIVE_FOLDER'], limit=None)
        songs_info = get_audio_files_from_folder(app.config['SONGS_FOLDER'], limit=None)  

        # Render the portfolio page
        return render_template('portfolio.html', 
                               acoustic_files_info=acoustic_files_info,
                               beats_files_info=beats_files_info,
                               demo_files_info=demo_files_info,
                               live_files_info=live_files_info,
                               songs_info=songs_info)
    except Exception as e:
        # Handle errors gracefully
        logger.error(f"Error fetching portfolio data: {e}")
        return jsonify({'error': 'Unable to fetch portfolio data'}), 500




@app.route('/store')
def store():
    return render_template('store.html')

if __name__ == '__main__':
    app.run(debug=True)
