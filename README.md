# Spotify-Voice-Assistant
# Spotify-Voice-Assistant
Spotify Voice Assistant using Python
Control your Spotify music using voice commands!
This Python-based assistant lets you play songs, albums, and artists just by speaking.

Features
* Voice recognition using your system microphone
* Smart Spotify search for tracks, albums, and artists
* Instant playback on your connected device
* Fallback to browser if playback fails
* Simple NLP for understanding commands like:
1) play <song name>
2) album <album name>
3) artist <artist name>

Requirements
* Python 3.8 or later
* Spotify Premium account
* Spotify desktop or mobile app running on a device
* The following Python libraries: spotipy, SpeechRecognition, pyaudio, pandas.

Also requires creation of a file project.txt containing following data:
* client_id=YOUR_CLIENT_ID
* client_secret=YOUR_CLIENT_SECRET
* redirect_uri=http://127.0.0.1:8000/callback
* scope=user-read-playback-state,user-modify-playback-state,user-read-currently-playing
* username=YOUR_SPOTIFY_USERNAME
* device_name=YOUR_DEVICE_NAME
