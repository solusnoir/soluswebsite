document.addEventListener('DOMContentLoaded', function () {
    const uploadForm = document.getElementById('upload-form');
    const songFileInput = document.getElementById('audio');
    const songKeySpan = document.getElementById('song-key');
    const songBpmSpan = document.getElementById('song-bpm');
    const errorMessageDiv = document.getElementById('error-message');

    uploadForm.addEventListener('submit', function (event) {
        event.preventDefault();  // Prevent page reload on form submit
        
        // Clear previous results
        errorMessageDiv.style.display = 'none';
        songKeySpan.textContent = 'N/A';
        songBpmSpan.textContent = 'N/A';

        // Ensure a file is selected
        const file = songFileInput.files[0];
        if (!file) {
            errorMessageDiv.textContent = "Please select a file.";
            errorMessageDiv.style.display = 'block';
            return;
        }

        // Create FormData to send the file
        const formData = new FormData();
        formData.append('audio_file', file);  // Ensure the field name is 'audio_file'

        // Send the POST request with the file
        fetch('/find-key', {
            method: 'POST',
            body: formData
        })
        .then(response => response.json())  // Expecting JSON response from the server
        .then(data => {
            if (data.error) {
                errorMessageDiv.textContent = `Error: ${data.error}`;
                errorMessageDiv.style.display = 'block';
            } else {
                songKeySpan.textContent = `${data.key} ${data.scale}`;
                songBpmSpan.textContent = data.bpm;
            }
        })
        .catch(error => {
            errorMessageDiv.textContent = `An unexpected error occurred: ${error}`;
            errorMessageDiv.style.display = 'block';
        });
    });
});
