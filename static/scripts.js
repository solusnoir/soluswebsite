async function fetchSongs() {
    try {
        const response = await fetch('/portfolio'); // Fetch from backend
        if (!response.ok) throw new Error('Failed to fetch songs');

        const data = await response.json();
        if (!data.songs_info || data.songs_info.length === 0) {
            displayNoSongsMessage(); // Display message when no songs are found
            return;
        }

        updateSongList(data.songs_info); // Update the DOM with audio files
    } catch (error) {
        console.error('Error fetching songs:', error);
        displayErrorMessage('Error loading songs.'); // Display error message
    }
}

// Update the DOM with the list of songs
function updateSongList(songs) {
    const songList = document.getElementById('song-list');
    if (!songList) return console.error("Element with ID 'song-list' not found");

    songList.innerHTML = ''; // Clear existing songs
    songs.forEach(song => {
        const listItem = createSongListItem(song);
        songList.appendChild(listItem);
    });
}

// Create a new list item for each song
function createSongListItem(song) {
    const listItem = document.createElement('li');
    const audioElement = document.createElement('audio');
    audioElement.controls = true;
    audioElement.src = song.url; // Set the URL of the audio file

    const downloadLink = document.createElement('a');
    downloadLink.href = song.download_url;
    downloadLink.textContent = `Download ${song.title}`;
    downloadLink.target = '_blank';

    listItem.appendChild(audioElement);
    listItem.appendChild(downloadLink);

    listItem.onclick = () => updatePlayer(song.url); // Update the player on click
    return listItem;
}

// Update the audio player with the selected song's URL
function updatePlayer(fileUrl) {
    const audioPlayer = document.getElementById('audio-player');
    const audioSource = document.getElementById('audio-source');

    audioSource.src = fileUrl; // Set the source of the audio player
    audioPlayer.load(); // Reload the player with the new file

    audioPlayer.play().catch((error) => console.error('Error playing audio:', error));
}

// Display message when no songs are available
function displayNoSongsMessage() {
    const songList = document.getElementById('song-list');
    if (songList) songList.innerHTML = 'No songs available.';
}

// Display error message when something goes wrong
function displayErrorMessage(message) {
    const songList = document.getElementById('song-list');
    if (songList) songList.innerHTML = message;
}

// Call fetchSongs when the page is loaded
document.addEventListener('DOMContentLoaded', fetchSongs);
