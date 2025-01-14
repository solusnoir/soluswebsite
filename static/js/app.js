document.getElementById('converterForm').addEventListener('submit', function(event) {
    event.preventDefault(); // Prevent the form from submitting normally
    
    let formData = new FormData(this);
    let format = document.getElementById('format').value;
    let fileInput = document.getElementById('audioFile');

    if (fileInput.files.length === 0) {
        alert("Please select a file.");
        return;
    }

    // Reset UI elements
    document.getElementById('statusMessage').innerHTML = "Converting...";
    document.getElementById('loadingBar').style.display = 'block';
    document.getElementById('downloadButton').style.display = 'none';

    let xhr = new XMLHttpRequest();
    xhr.open('POST', '/convert', true);
    xhr.upload.onprogress = function(event) {
        if (event.lengthComputable) {
            let percent = (event.loaded / event.total) * 100;
            document.getElementById('loadingBar').style.width = percent + '%';
        }
    };

    xhr.onload = function() {
        if (xhr.status === 200) {
            // Success - Show download button
            let response = JSON.parse(xhr.responseText);
            document.getElementById('statusMessage').innerHTML = "Conversion Complete!";
            document.getElementById('loadingBar').style.display = 'none';
            document.getElementById('downloadButton').style.display = 'inline-block';
            document.getElementById('downloadButton').setAttribute('data-url', response.download_url);
        } else {
            document.getElementById('statusMessage').innerHTML = "Conversion failed!";
            document.getElementById('loadingBar').style.display = 'none';
        }
    };

    xhr.send(formData);
});

function downloadFile() {
    let downloadButton = document.getElementById('downloadButton');
    let downloadUrl = downloadButton.getAttribute('data-url');
    let link = document.createElement('a');
    link.href = downloadUrl;
    link.download = 'converted_audio';
    link.click();
}
