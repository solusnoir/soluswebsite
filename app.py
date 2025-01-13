from flask import Flask, render_template, request, jsonify, send_from_directory, url_for
import os
import logging
from dotenv import load_dotenv
from convert import convert_audio  # Import the convert_audio function from convert.py
from find_key import find_key  # Import the find_key function for key and BPM detection

# Load environment variables from .env file
load_dotenv()

# Configuration class
class Config:
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    ACOUSTIC_FOLDER = os.path.join(BASE_DIR, 'static', 'acoustic')
    BEATS_FOLDER = os.path.join(BASE_DIR, 'static', 'beats')
    DEMO_FOLDER = os.path.join(BASE_DIR, 'static', 'demos')
    LIVE_FOLDER = os.path.join(BASE_DIR, 'static', 'live')
    SONGS_FOLDER = os.path.join(BASE_DIR, 'static', 'songs')
    UPLOAD_FOLDER = os.path.join(BASE_DIR, 'uploads')
    ALLOWED_EXTENSIONS = {'wav', 'mp3', 'ogg', 'm4a'}
    VISITOR_FILE = os.path.join(BASE_DIR, 'visitor_count.json')

    FLASK_ENV = os.getenv('FLASK_ENV', 'production')
    SECRET_KEY = os.getenv('SECRET_KEY', 'your-secret-key')

app = Flask(__name__)
app.config.from_object(Config)

# Initialize logging
logging.basicConfig(
    level=logging.DEBUG if app.config['FLASK_ENV'] == 'development' else logging.INFO,
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
os.makedirs(app.config['SONGS_FOLDER'], exist_ok=True)
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Helper function to list audio files
def get_audio_files_info(folder):
    audio_files = []
    for filename in os.listdir(folder):
        if filename.split('.')[-1].lower() in Config.ALLOWED_EXTENSIONS:
            audio_files.append({
                'name': filename,
                'url': url_for('static', filename=os.path.join(folder.split('/')[-1], filename)),
                'download_url': url_for('download_file', folder=folder.split('/')[-1], filename=filename)
            })
    return audio_files

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/portfolio')
def portfolio():
    beats_files_info = get_audio_files_info(app.config['BEATS_FOLDER'])
    demo_files_info = get_audio_files_info(app.config['DEMO_FOLDER'])
    live_files_info = get_audio_files_info(app.config['LIVE_FOLDER'])
    songs_info = get_audio_files_info(app.config['SONGS_FOLDER'])
    acoustic_files_info = get_audio_files_info(app.config['ACOUSTIC_FOLDER'])
    return render_template(
        'portfolio.html',
        beats_files_info=beats_files_info,
        demo_files_info=demo_files_info,
        live_files_info=live_files_info,
        songs_info=songs_info,
        acoustic_files_info=acoustic_files_info
    )

@app.route('/store')
def store():
    return render_template('store.html')

@app.route('/convert')
def convert_page():
    return render_template('convert.html')

@app.route('/convert', methods=['POST'])
def convert():
    return convert_audio()

@app.route('/find-key')
def find_key_page():
    return render_template('find-key.html')

@app.route('/find-key', methods=['POST'])
def find_key_route():
    if 'audio' not in request.files:
        return jsonify({'success': False, 'message': 'No file uploaded'}), 400

    file = request.files['audio']
    audio_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    file.save(audio_path)

    try:
        # Detect key and BPM using the find_key function
        detection_result = find_key(audio_path)
        return jsonify({'success': True, **detection_result})
    except Exception as e:
        logger.error(f"Error during key/BPM detection: {e}")
        return jsonify({'success': False, 'message': str(e)}), 500

@app.route('/download/<folder>/<filename>')
def download_file(folder, filename):
    folder_path = os.path.join(app.config.BASE_DIR, 'static', folder)
    return send_from_directory(folder_path, filename, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True, port=5001)
