async function fetchSongs() {
    try {
        const response = await fetch('/portfolio');
        if (!response.ok) throw new Error('Failed to fetch songs');

        const data = await response.json();

        if (!data.demo_files_info || data.demo_files_info.length === 0) {
            displayNoSongsMessage();
            return;
        }

        updateSongList(data.demo_files_info);
    } catch (error) {
        console.error('Error fetching songs:', error);
        displayErrorMessage('Error loading songs.');
    }
}

function updateSongList(songs) {
    const songList = document.getElementById('song-list');
    songList.innerHTML = '';

    if (songs.length === 0) {
        displayNoSongsMessage();
    } else {
        songs.forEach(song => {
            const listItem = createSongListItem(song);
            songList.appendChild(listItem);
        });
    }
}

function createSongListItem(song) {
    const listItem = document.createElement('li');
    
    const audioElement = document.createElement('audio');
    audioElement.controls = true;
    audioElement.src = song.url;

    const downloadLink = document.createElement('a');
    downloadLink.href = song.download_url;
    downloadLink.textContent = `Download ${song.name}`;
    downloadLink.target = '_blank';

    listItem.appendChild(audioElement);
    listItem.appendChild(downloadLink);
    listItem.onclick = () => updatePlayer(song.url);

    return listItem;
}

function updatePlayer(fileUrl) {
    const audioPlayer = document.getElementById('audio-player');
    const audioSource = document.getElementById('audio-source');
    audioSource.src = fileUrl;
    audioPlayer.load();
    audioPlayer.play();
}

function displayNoSongsMessage() {
    const songList = document.getElementById('song-list');
    songList.innerHTML = 'No songs available.';
}

function displayErrorMessage(message) {
    const songList = document.getElementById('song-list');
    songList.innerHTML = message;
}

document.addEventListener('DOMContentLoaded', fetchSongs);
