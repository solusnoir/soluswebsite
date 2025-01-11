document.addEventListener('DOMContentLoaded', () => {
    // Get current page name from the URL path
    const currentPage = window.location.pathname.split('/').pop();
  
    // Menu Toggle for Mobile
    const menuToggle = document.querySelector('.menu-toggle');
    const nav = document.querySelector('.nav');
    
    // Scroll Event to hide/show navbar
    let lastScrollTop = 0;  // Variable to track scroll position
    const header = document.querySelector('.header');
    
    window.addEventListener('scroll', function () {
      let scrollPosition = window.scrollY;
      const introHeight = document.getElementById('intro') ? document.getElementById('intro').clientHeight : 0;
  
      // Only toggle visibility after intro section for certain pages (like portfolio, store, etc.)
      if (scrollPosition > introHeight || currentPage !== 'index.html') {
        header.classList.add('visible');
      } else {
        header.classList.remove('visible');
      }
  
      // Hide navbar on scroll down, show on scroll up
      if (scrollPosition > lastScrollTop && scrollPosition > introHeight) {
        header.style.top = '-100px'; // Scroll down: hide navbar
      } else {
        header.style.top = '0'; // Scroll up: show navbar
      }
  
      lastScrollTop = scrollPosition <= 0 ? 0 : scrollPosition; // Prevent negative scroll
    });
  
    // Mobile Menu Toggle
    menuToggle.addEventListener('click', () => {
      nav.classList.toggle('active');  // Toggle the menu visibility
      menuToggle.classList.toggle('open');  // Update toggle button appearance
    });
  });
  
  // Fetch Song Data and Update the Player
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
  
    if (song.download_url) { // Only create download link if the URL exists
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
  
  // Initialize by fetching songs only, no navbar reset
  document.addEventListener('DOMContentLoaded', async () => {
    // Fetch and display songs
    await fetchSongs();
  });
  