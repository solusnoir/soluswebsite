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
        console.error('Error fetching songs:', error.message);
        displayErrorMessage('Error loading songs.');
    }
}

function updateSongList(songs) {
    const songList = document.getElementById('song-list');
    const fragment = document.createDocumentFragment();

    if (!songs.length) {
        displayNoSongsMessage();
    } else {
        songs.forEach(song => {
            const listItem = createSongListItem(song);
            fragment.appendChild(listItem);
        });
        songList.innerHTML = ''; // Clear the list
        songList.appendChild(fragment);
    }
}

function createSongListItem(song) {
    const listItem = document.createElement('li');
    
    const audioElement = document.createElement('audio');
    audioElement.controls = true;
    audioElement.src = song.url;

    if (song.download_url) {  // Only create download link if the URL exists
        const downloadLink = document.createElement('a');
        downloadLink.href = song.download_url;
        downloadLink.textContent = `Download ${song.name}`;
        downloadLink.target = '_blank';
        listItem.appendChild(downloadLink);
    }

    listItem.appendChild(audioElement);
    listItem.onclick = () => updatePlayer(song.url);

    return listItem;
}

function updatePlayer(fileUrl) {
    const audioPlayer = document.getElementById('audio-player');
    const audioSource = document.getElementById('audio-source');
    
    // Prevent playing a new song if the current one is already playing
    if (audioPlayer.paused || audioPlayer.currentSrc !== fileUrl) {
        audioSource.src = fileUrl;
        audioPlayer.load();
        audioPlayer.play();
    }
}

function displayNoSongsMessage() {
    const songList = document.getElementById('song-list');
    if (songList) {
        songList.innerHTML = 'No songs available.';
    }
}

function displayErrorMessage(message) {
    const songList = document.getElementById('song-list');
    if (songList) {
        songList.innerHTML = message;
    }
}

document.addEventListener('DOMContentLoaded', async () => {
    await fetchSongs();
});
