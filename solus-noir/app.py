import os
import logging
from flask import Flask, render_template, request, jsonify, redirect, url_for
from dotenv import load_dotenv
import json

# Initialize logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('app.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Load environment variables from .env file for local development
load_dotenv()

# Initialize Flask app
app = Flask(__name__)

# Configuration class
class Config:
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    ACOUSTIC_FOLDER = os.path.join(BASE_DIR, 'static', 'acoustic')  # Path for acoustic folder
    BEATS_FOLDER = os.path.join(BASE_DIR, 'static', 'beats')  # Path for beats folder
    DEMO_FOLDER = os.path.join(BASE_DIR, 'static', 'demos')  # Path for demos folder
    ALLOWED_EXTENSIONS = {'wav', 'mp3', 'ogg'}  # Allowed audio file extensions
    VISITOR_FILE = 'visitor_count.json'

    # Heroku-specific environment variables (with defaults for local development)
    FLASK_ENV = os.getenv('FLASK_ENV', 'development')  # Set FLASK_ENV to production on Heroku
    SECRET_KEY = os.getenv('SECRET_KEY', 'your-secret-key')  # Replace with a secure key for production

app.config.from_object(Config)

# Create required directories
os.makedirs(app.config['ACOUSTIC_FOLDER'], exist_ok=True)
os.makedirs(app.config['BEATS_FOLDER'], exist_ok=True)
os.makedirs(app.config['DEMO_FOLDER'], exist_ok=True)

# Function to get the current visitor count from the visitor_count.json file
def get_visitor_count():
    try:
        if os.path.exists(app.config['VISITOR_FILE']):
            with open(app.config['VISITOR_FILE'], 'r') as f:
                data = json.load(f)
            return data.get('count', 0)  # Default to 0 if 'count' is missing
        else:
            return 0  # Return 0 if the file doesn't exist yet
    except Exception as e:
        logger.error(f"Error reading visitor count: {str(e)}")
        return 0  # Return 0 if there's an error

# Function to get a preview of the audio files (only a few files for homepage)
def get_audio_files_from_folder(folder_path, limit=2):
    audio_files_info = []
    if os.path.exists(folder_path):
        files = [f for f in os.listdir(folder_path) if f.endswith(tuple(app.config['ALLOWED_EXTENSIONS']))]
        for filename in files[:limit]:  # Limit to a few files for preview
            file_path = os.path.join(folder_path, filename)
            audio_files_info.append({
                'name': filename,
                'url': f'/static/{folder_path.split("/")[-1]}/{filename}',
                'download_url': f'/static/{folder_path.split("/")[-1]}/{filename}',
                'created_time': '2025-01-01',  # Optional: date of creation
            })
    return audio_files_info

# Routes
@app.route('/')
def home():
    increment_visitor_count()  # Increment visitor count on each visit
    
    # Fetch previews for the homepage
    acoustic_files_info = get_audio_files_from_folder(app.config['ACOUSTIC_FOLDER'])
    beats_files_info = get_audio_files_from_folder(app.config['BEATS_FOLDER'])
    demo_files_info = get_audio_files_from_folder(app.config['DEMO_FOLDER'])

    # Render homepage with preview data
    return render_template('index.html', acoustic_files_info=acoustic_files_info, 
                           beats_files_info=beats_files_info, demo_files_info=demo_files_info,
                           visitor_count=get_visitor_count())

@app.route('/portfolio')
def portfolio():
    try:
        # Get all audio files from each folder: acoustic, beats, demos
        acoustic_files_info = get_audio_files_from_folder(app.config['ACOUSTIC_FOLDER'], limit=None)
        beats_files_info = get_audio_files_from_folder(app.config['BEATS_FOLDER'], limit=None)
        demo_files_info = get_audio_files_from_folder(app.config['DEMO_FOLDER'], limit=None)

        # Pass the list of audio files to the portfolio template
        return render_template('portfolio.html', acoustic_files_info=acoustic_files_info, 
                               beats_files_info=beats_files_info, demo_files_info=demo_files_info)

    except Exception as e:
        logger.error(f"Error fetching files from folders: {str(e)}")
        return render_template('portfolio.html', error="Failed to retrieve audio files")

@app.route('/store')
def store():
    # Render the store page with a coming soon message
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
    port = int(os.getenv('PORT', 5001))  # Use port 5001 by default, can be changed
    app.run(debug=True, port=port)
