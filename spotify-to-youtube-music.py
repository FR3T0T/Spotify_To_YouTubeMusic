import os
import sys
import json
import time
import base64
import webbrowser
from urllib.parse import urlencode
import http.server
import socketserver
import threading
import requests

# Import ytmusicapi with error handling
try:
    from ytmusicapi import YTMusic
except ImportError:
    print("Error: ytmusicapi is not installed. Install it using: pip install ytmusicapi")
    sys.exit(1)

print("=" * 60)
print("Spotify to YouTube Music Playlist Transfer")
print("=" * 60)

# Spotify API credentials - you need to fill these in
SPOTIFY_CLIENT_ID = '8033620ee23a4b2d953541864e034a7a'
SPOTIFY_CLIENT_SECRET = 'be42e5607bc54d63b1ff72123e316311'

# Check credentials
if SPOTIFY_CLIENT_ID == 'YOUR_SPOTIFY_CLIENT_ID' or SPOTIFY_CLIENT_SECRET == 'YOUR_SPOTIFY_CLIENT_SECRET':
    print("\nERROR: You need to set your Spotify API credentials in the script.")
    print("1. Go to https://developer.spotify.com/dashboard/applications")
    print("2. Create a new application")
    print("3. Get your Client ID and Client Secret")
    print("4. Add http://localhost:8888/callback as a Redirect URI in your app settings")
    print("5. Update the SPOTIFY_CLIENT_ID and SPOTIFY_CLIENT_SECRET variables in this script")
    sys.exit(1)

# OAuth setup
REDIRECT_PORT = 8888
REDIRECT_URI = f'http://localhost:{REDIRECT_PORT}/callback'
AUTH_CODE = None
SERVER = None

# Callback handler for Spotify OAuth
class CallbackHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        global AUTH_CODE, SERVER
        
        if '?code=' in self.path:
            AUTH_CODE = self.path.split('?code=')[1].split('&')[0]
            
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(b"<html><body><h1>Authentication Successful!</h1><p>You can close this window now.</p></body></html>")
            
            SERVER.shutdown()
        else:
            self.send_response(400)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(b"<html><body><h1>Authentication Failed</h1></body></html>")
    
    def log_message(self, format, *args):
        # Suppress server logs
        return

# Start OAuth server for Spotify
def start_auth_server():
    global SERVER
    SERVER = socketserver.TCPServer(("", REDIRECT_PORT), CallbackHandler)
    try:
        SERVER.serve_forever()
    except:
        pass

# Get Spotify auth code
def get_spotify_auth_code():
    global AUTH_CODE
    
    # Create authorization URL
    auth_params = {
        'client_id': SPOTIFY_CLIENT_ID,
        'response_type': 'code',
        'redirect_uri': REDIRECT_URI,
        'scope': 'playlist-read-private playlist-read-collaborative'
    }
    auth_url = 'https://accounts.spotify.com/authorize?' + urlencode(auth_params)
    
    # Start server for callback
    server_thread = threading.Thread(target=start_auth_server)
    server_thread.daemon = True
    server_thread.start()
    
    # Open browser for user authentication
    print("\nOpening your browser to authorize Spotify access...")
    webbrowser.open(auth_url)
    
    # Wait for authentication
    print("Waiting for authorization...")
    timeout = 300  # 5 minutes
    start_time = time.time()
    
    while not AUTH_CODE and time.time() - start_time < timeout:
        time.sleep(1)
        
    if not AUTH_CODE:
        print("\nError: Authentication timed out")
        sys.exit(1)
        
    return AUTH_CODE

# Get Spotify access token
def get_spotify_token(auth_code):
    # Encode client ID and secret
    auth_header = base64.b64encode(f"{SPOTIFY_CLIENT_ID}:{SPOTIFY_CLIENT_SECRET}".encode()).decode()
    
    headers = {
        'Authorization': f'Basic {auth_header}',
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    
    data = {
        'grant_type': 'authorization_code',
        'code': auth_code,
        'redirect_uri': REDIRECT_URI
    }
    
    try:
        response = requests.post('https://accounts.spotify.com/api/token', headers=headers, data=data)
        response.raise_for_status()
        return response.json()['access_token']
    except Exception as e:
        print(f"\nError getting Spotify access token: {str(e)}")
        if hasattr(response, 'text'):
            print(f"Response: {response.text}")
        sys.exit(1)

# Get user's Spotify playlists
def get_spotify_playlists(token):
    print("\nFetching your Spotify playlists...")
    
    headers = {'Authorization': f'Bearer {token}'}
    playlists = []
    url = 'https://api.spotify.com/v1/me/playlists?limit=50'
    
    try:
        while url:
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            data = response.json()
            playlists.extend(data['items'])
            url = data.get('next')
            
        return playlists
    except Exception as e:
        print(f"\nError fetching playlists: {str(e)}")
        sys.exit(1)

# Display user's playlists
def display_playlists(playlists):
    print(f"\nFound {len(playlists)} playlists:")
    print("-" * 60)
    
    for i, playlist in enumerate(playlists):
        track_count = playlist['tracks']['total']
        print(f"{i+1}. {playlist['name']} ({track_count} tracks)")

# Select a playlist
def select_playlist(playlists):
    while True:
        try:
            choice = int(input("\nEnter the number of the playlist you want to transfer: "))
            if 1 <= choice <= len(playlists):
                return playlists[choice - 1]
            else:
                print(f"Please enter a number between 1 and {len(playlists)}")
        except ValueError:
            print("Please enter a valid number")
        except KeyboardInterrupt:
            print("\nOperation cancelled")
            sys.exit(0)

# Get tracks from a playlist
def get_playlist_tracks(token, playlist_id):
    print("\nFetching playlist tracks...")
    
    headers = {'Authorization': f'Bearer {token}'}
    tracks = []
    url = f'https://api.spotify.com/v1/playlists/{playlist_id}/tracks?limit=100'
    
    try:
        while url:
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            data = response.json()
            
            for item in data['items']:
                if item['track']:
                    track = {
                        'name': item['track']['name'],
                        'artists': [artist['name'] for artist in item['track']['artists']]
                    }
                    tracks.append(track)
            
            url = data.get('next')
        
        print(f"✓ Found {len(tracks)} tracks in the playlist")
        return tracks
    except Exception as e:
        print(f"\nError fetching tracks: {str(e)}")
        sys.exit(1)

# Get ytmusicapi version
def get_ytmusicapi_version():
    try:
        import pkg_resources
        return pkg_resources.get_distribution("ytmusicapi").version
    except:
        return "unknown"

# Set up YouTube Music - Improved version with better error handling
def setup_youtube_music():
    print("\nSetting up YouTube Music authentication...")
    
    # Check for existing authentication files
    auth_files = []
    if os.path.exists("oauth.json"):
        auth_files.append(("oauth.json", "OAuth"))
    if os.path.exists("headers_auth.json"):
        auth_files.append(("headers_auth.json", "Headers"))
    
    # Try to use existing authentication
    for auth_file, auth_type in auth_files:
        try:
            print(f"\nTrying existing {auth_type} authentication from {auth_file}...")
            ytmusic = YTMusic(auth_file)
            # Test the connection by making a simple API call
            try:
                ytmusic.get_library_playlists(limit=1)
                print(f"✓ Successfully authenticated with YouTube Music using {auth_type}!")
                return ytmusic
            except Exception as e:
                print(f"× Existing {auth_type} authentication failed: {str(e)}")
        except Exception as e:
            print(f"× Error loading {auth_type} authentication: {str(e)}")
    
    print("\n→ Need to create new YouTube Music authentication")
    
    version = get_ytmusicapi_version()
    print(f"ytmusicapi version: {version}")
    
    # Try OAuth method first (most reliable)
    try:
        print("\nAttempting OAuth authentication (Method 1)...")
        try:
            # For newer versions of ytmusicapi
            YTMusic.oauth(filepath="oauth.json")
            print("✓ OAuth setup completed")
            return YTMusic("oauth.json")
        except AttributeError:
            try:
                # Alternative method name
                YTMusic.oauth_setup(filepath="oauth.json")
                print("✓ OAuth setup completed")
                return YTMusic("oauth.json")
            except AttributeError:
                print("× OAuth method not available in your ytmusicapi version")
    except Exception as e:
        print(f"× OAuth setup error: {str(e)}")
    
    # Try browser setup method
    try:
        print("\nAttempting browser setup (Method 2)...")
        try:
            YTMusic.setup(filepath="headers_auth.json")
            print("✓ Browser setup completed")
            return YTMusic("headers_auth.json")
        except AttributeError:
            print("× Browser setup method not available in your ytmusicapi version")
    except Exception as e:
        print(f"× Browser setup error: {str(e)}")
    
    # Manual headers method as last resort
    print("\nAttempting manual headers setup (Method 3)...")
    print("\nPlease follow these steps to get your authentication headers:")
    print("1. Open YouTube Music in your browser (music.youtube.com)")
    print("2. Login if you're not already logged in")
    print("3. Open developer tools (F12 or right-click > Inspect)")
    print("4. Go to the Network tab")
    print("5. Refresh the page")
    print("6. Find any request to 'youtubei/v1' (e.g., browse, next, search)")
    print("7. Right-click the request > Copy > Copy as cURL")
    print("8. Paste the copied cURL command below\n")
    
    curl_command = input("Paste the cURL command here: ")
    
    if not curl_command.strip():
        print("\nNo input provided.")
        print("\nAlternative methods:")
        print("1. Run in a separate terminal: python -m ytmusicapi oauth")
        print("2. Follow the instructions to create oauth.json")
        print("3. Run this script again")
        sys.exit(1)
    
    try:
        # Try to set up auth from the cURL command
        with open("headers_auth.json", "w") as f:
            f.write(curl_command)
        
        # Use the setup_from_file method if available
        try:
            YTMusic.setup_from_file("headers_auth.json")
            os.remove("headers_auth.json")  # Remove the temporary file
        except AttributeError:
            # If not available, keep the file as is (older ytmusicapi versions)
            pass
        
        return YTMusic("headers_auth.json")
    except Exception as e:
        print(f"\nError with manual setup: {str(e)}")
        print("\nPlease try the alternative method:")
        print("1. Run in a separate terminal: python -m ytmusicapi oauth")
        print("2. Follow the instructions to create oauth.json")
        print("3. Run this script again")
        sys.exit(1)

# Create YouTube Music playlist and add tracks with improved error handling and progress display
def transfer_to_youtube_music(ytmusic, playlist_name, tracks):
    # Create new playlist
    print(f"\nCreating YouTube Music playlist: '{playlist_name} (from Spotify)'...")
    
    try:
        playlist_id = ytmusic.create_playlist(
            title=f"{playlist_name} (from Spotify)",
            description="Transferred from Spotify",
            privacy_status="PRIVATE"
        )
        
        print(f"✓ Created new playlist with ID: {playlist_id}")
    except Exception as e:
        print(f"× Error creating playlist: {str(e)}")
        return
    
    print("\nTransferring tracks (this may take a while)...")
    print("-" * 60)
    
    # Track counters
    total = len(tracks)
    success = 0
    failed = 0
    
    # Process each track
    for i, track in enumerate(tracks):
        track_name = track['name']
        artists = ", ".join(track['artists'])
        search_query = f"{track_name} {artists}"
        
        print(f"[{i+1}/{total}] Searching for: {track_name} by {artists}")
        
        try:
            # Search for the track
            search_results = ytmusic.search(search_query, filter="songs", limit=3)
            
            if search_results:
                # Sometimes the first result isn't the best match, so we'll check the top 3
                # and choose the one that seems most relevant
                best_match = search_results[0]
                video_id = best_match["videoId"]
                
                # Add track to playlist
                status = ytmusic.add_playlist_items(playlist_id, [video_id])
                success += 1
                print(f"✓ Added to playlist: {best_match.get('title', 'Unknown')} by {best_match.get('artists', [{'name': 'Unknown'}])[0]['name']}")
            else:
                # Try a simpler search with just the track name
                print(f"  Trying simpler search with just track name...")
                search_results = ytmusic.search(track_name, filter="songs", limit=1)
                
                if search_results:
                    video_id = search_results[0]["videoId"]
                    status = ytmusic.add_playlist_items(playlist_id, [video_id])
                    success += 1
                    print(f"✓ Added to playlist (alternate match)")
                else:
                    print(f"× Could not find track")
                    failed += 1
                
            # Sleep to avoid rate limiting
            time.sleep(1)
            
        except Exception as e:
            print(f"× Error: {str(e)}")
            failed += 1
            
            # If we encounter too many errors in a row, pause to avoid triggering rate limits
            if failed > 5 and failed % 5 == 0:
                pause_time = 30
                print(f"\nToo many errors, pausing for {pause_time} seconds to avoid rate limits...")
                time.sleep(pause_time)
    
    print("-" * 60)
    print(f"\nTransfer summary: {success}/{total} tracks added, {failed} failed")
    print(f"\nYour new playlist is ready! You can access it in YouTube Music.")

# Main execution
if __name__ == "__main__":
    try:
        # Authenticate with Spotify
        print("\nAuthenticating with Spotify...")
        auth_code = get_spotify_auth_code()
        spotify_token = get_spotify_token(auth_code)
        print("✓ Successfully authenticated with Spotify!")
        
        # Get user's Spotify playlists
        playlists = get_spotify_playlists(spotify_token)
        display_playlists(playlists)
        
        # Let user select a playlist
        selected_playlist = select_playlist(playlists)
        
        # Get tracks from the selected playlist
        tracks = get_playlist_tracks(spotify_token, selected_playlist['id'])
        
        # Authenticate with YouTube Music
        ytmusic = setup_youtube_music()
        
        # Create YouTube Music playlist and add tracks
        transfer_to_youtube_music(ytmusic, selected_playlist['name'], tracks)
        
        print("\nTransfer completed!")
        print("\nThanks for using the Spotify to YouTube Music Playlist Transfer tool!")
        
    except KeyboardInterrupt:
        print("\nTransfer cancelled by user")
        sys.exit(0)
    except Exception as e:
        print(f"\nUnexpected error: {str(e)}")
        sys.exit(1)