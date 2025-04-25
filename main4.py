import pandas as pd
from speech_recognition import Microphone, Recognizer, UnknownValueError
import spotipy as sp
from spotipy.oauth2 import SpotifyOAuth
from pepper import *
import webbrowser

# === Load credentials from project.txt ===
setup = pd.read_csv(r'C:\Users\Hp-PC\Desktop\Spotify_Assist\project.txt', sep='=', index_col=0, header=None)
setup = setup.squeeze()

client_id = setup['client_id']
client_secret = setup['client_secret']
device_name = setup['device_name']
redirect_uri = setup['redirect_uri']
scope = setup['scope']
username = setup['username']

# === Connect to Spotify with OAuth ===
auth_manager = SpotifyOAuth(
    client_id=client_id,
    client_secret=client_secret,
    redirect_uri=redirect_uri,
    scope=scope,
    username=username
)
spotify = sp.Spotify(auth_manager=auth_manager)

# === Confirm login ===
me = spotify.me()
print(f"✅ Logged in as: {me['display_name']} ({me['email']})")

# === Find the target device ===
devices = spotify.devices()
deviceID = None
print("🔍 Available Devices:")
for d in devices['devices']:
    print(" -", d['name'])
    if d['name'].strip().lower() == device_name.strip().lower():
        deviceID = d['id']

if not deviceID:
    print(f"❌ Device '{device_name}' not found. Please check the name in project.txt.")
    exit()

# === Setup microphone (default system mic) ===
r = Recognizer()
m = None
input_mic = None  # auto-select default mic

# Auto-select system microphone
for i, microphone_name in enumerate(Microphone.list_microphone_names()):
    print(f"[{i}] {microphone_name}")
    if "microphone" in microphone_name.lower():
        m = Microphone(device_index=i)
        print(f"🎤 Using microphone: {microphone_name}")
        break

if m is None:
    print("❌ Could not find a working microphone.")
    exit()

# === Main voice command loop ===
while True:
    print("🎧 Listening...")
    with m as source:
        r.adjust_for_ambient_noise(source)
        audio = r.listen(source)

    try:
        command = r.recognize_google(audio).lower()
        print(f"📢 Command: {command}")
    except UnknownValueError:
        print("🤷 Couldn't understand. Try again.")
        continue

    words = command.split()
    if len(words) < 2:
        print("❗ Say: play / album / artist + name")
        continue

    name = ' '.join(words[1:])
    uri = None

    try:
        if words[0] == 'album':
            uri = get_album_uri(spotify, name)
            play_album(spotify, deviceID, uri)
        elif words[0] == 'artist':
            uri = get_artist_uri(spotify, name)
            play_artist(spotify, deviceID, uri)
        elif words[0] == 'play':
            uri = get_track_uri(spotify, name)
            print(f"🎶 URI: {uri}")
            try:
                spotify.start_playback(device_id=deviceID, uris=[uri])
                print("▶️ Now playing...")
            except Exception as e:
                print("⚠️ Spotify playback failed, opening in browser...")
                print(e)
                track_id = uri.split(":")[-1]
                webbrowser.open(f"https://open.spotify.com/track/{track_id}")
        else:
            print('❗ Start your command with "play", "album" or "artist".')
    except InvalidSearchError:
        print("❌ Couldn't find that. Try again.")
