from flask import Flask, render_template, request, jsonify
import os
import tempfile
import shutil
import subprocess
import traceback
import uuid

# Set ffmpeg path if it's not detected automatically (adjust as needed)
FFMPEG_PATH = "/opt/homebrew/bin/ffmpeg"  # Path to ffmpeg on your local system

# Check if we're on Heroku, and if so, let the buildpack handle ffmpeg
FFMPEG_EXEC = FFMPEG_PATH if os.path.exists(FFMPEG_PATH) else "ffmpeg"

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/convert', methods=['POST'])
def convert_audio():
    if 'audioFile' not in request.files:
        return jsonify({"error": "No file part"}), 400
    file = request.files['audioFile']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    # Get the format to convert to
    format = request.form['format']

    # Save the uploaded file temporarily
    try:
        with tempfile.NamedTemporaryFile(delete=False) as temp_file:
            file.save(temp_file.name)

            # Get the original file name without the extension
            original_filename = os.path.splitext(file.filename)[0]

            # Create a unique temporary file for the output with the new file name and format
            output_file_name = f"{original_filename}.{format}"  # Keep original name with new extension
            output_file_path = os.path.join(tempfile.gettempdir(), output_file_name)

            # Convert the audio using ffmpeg
            try:
                print(f"Converting {temp_file.name} to {output_file_path} using {FFMPEG_EXEC}")
                if format == 'wav':
                    command = [
                        FFMPEG_EXEC,
                        '-y',  # Automatically overwrite if the file exists
                        '-i', temp_file.name,
                        '-acodec', 'pcm_s16le',  # WAV codec
                        '-ar', '44100',  # Set sample rate (adjust if needed)
                        '-ac', '2',  # Stereo output
                        output_file_path
                    ]
                elif format == 'm4a':
                    command = [
                        FFMPEG_EXEC, 
                        '-y', 
                        '-i', temp_file.name, 
                        '-acodec', 'aac',  # Use 'aac' for m4a
                        '-b:a', '192k',  # Audio bitrate (adjust as needed)
                        output_file_path
                    ]
                else:  # For mp3
                    command = [
                        FFMPEG_EXEC, 
                        '-y', 
                        '-i', temp_file.name, 
                        '-acodec', 'libmp3lame',  # Use 'libmp3lame' for mp3
                        '-b:a', '192k',  # Audio bitrate (adjust as needed)
                        output_file_path
                    ]
                subprocess.run(command, check=True)
                print(f"Audio converted successfully to {format}.")
            except subprocess.CalledProcessError as e:
                print(f"Error during ffmpeg conversion: {e}")
                return jsonify({"error": f"Error converting audio file: {e}"}), 500

            # Move the output file to the static folder for downloading
            static_output_path = os.path.join('static', output_file_name)  # Use original name
            shutil.move(output_file_path, static_output_path)

            # Send the URL for download as a JSON response
            download_url = f"/static/{output_file_name}"

            # Cleanup: Remove the temporary files after use
            os.remove(temp_file.name)
            # No need to remove the output file as it was moved

            return jsonify({'download_url': download_url})

    except Exception as e:
        print(f"Unexpected error: {e}")
        traceback.print_exc()
        return jsonify({"error": f"An unexpected error occurred: {e}"}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5001)
