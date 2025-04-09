# Spotify to YouTube Music Playlist Transfer

This tool allows you to transfer your Spotify playlists to YouTube Music automatically. It uses the Spotify and YouTube Music APIs to fetch your playlists from Spotify and recreate them on YouTube Music.

## Author

Created by FR3T0T & Frederik T.

## Features

- Authenticate with both Spotify and YouTube Music
- View all your Spotify playlists
- Transfer any playlist with all tracks
- Intelligent song matching between platforms
- Track transfer progress and success rate

## Prerequisites

- Python 3.7 or higher
- A Spotify account
- A YouTube Music account
- Basic knowledge of using the command line

## Installation

1. Clone or download this repository
2. Install the required Python packages:

```bash
pip install ytmusicapi requests
```

## Setup

### Step 1: Set Up Spotify API Credentials

Before using the script, you need to register your application with Spotify to get API credentials:

1. Go to the [Spotify Developer Dashboard](https://developer.spotify.com/dashboard/)
2. Log in with your Spotify account
3. Click on "Create An App"
4. Fill in the app name and description (e.g., "Playlist Transfer Tool")
5. Check the terms of service and click "Create"
6. In your app's dashboard, you'll see your **Client ID**
7. Click "Show Client Secret" to reveal your **Client Secret**
8. Click "Edit Settings" and add `http://localhost:8888/callback` as a Redirect URI, then save

Now open `spotify-to-youtube-music.py` in a text editor and replace:
```python
SPOTIFY_CLIENT_ID = 'SPOTIFY_CLIENT_ID'
SPOTIFY_CLIENT_SECRET = 'SPOTIFY_CLIENT_SECRET'
```
with your actual credentials:
```python
SPOTIFY_CLIENT_ID = 'your_actual_client_id_here'
SPOTIFY_CLIENT_SECRET = 'your_actual_client_secret_here'
```

### Step 2: Understanding YouTube Music Authentication

YouTube Music doesn't have an official public API, so this tool uses an unofficial API that requires authentication cookies from your browser. The authentication process involves copying these cookies and authorization headers from your browser's developer tools.

## Usage

### Step 1: Set Up YouTube Music Authentication

Run the authentication helper:

```bash
python youtube_auth_helper.py
```

This will guide you through the process of copying authentication data from your browser. Here's what happens:

1. The script will prompt you to open YouTube Music in your browser
2. Make sure you're logged into YouTube Music
3. Open your browser's developer tools:
   - Chrome/Edge: Press F12 or right-click and select "Inspect"
   - Firefox: Press F12 or right-click and select "Inspect Element"

4. In the developer tools, go to the Network tab
5. Refresh the YouTube Music page
6. Look for requests to `browse`, `next`, or any YouTube Music API endpoints
7. Click on one of these requests
8. In the Headers tab, find the "Cookie" header under Request Headers
9. Right-click on the value and select "Copy value"
10. Paste this entire string when prompted by the script
11. Similarly, find the "Authorization" header and copy its value
12. Paste this when prompted

The script will create a `headers_auth.json` file and test if the authentication works.

#### YouTube Music Authentication Troubleshooting

If authentication fails:

- Make sure you're logged into YouTube Music in your browser
- Try copying the cookies and Authorization header again
- Ensure you're copying the entire cookie string, not just part of it
- If you see errors about missing cookies, make sure you're copying from YouTube Music (music.youtube.com) and not regular YouTube

### Step 2: Verify Authentication

You can test if your authentication is working correctly:

```bash
python test_auth.py
```

This script will check if you can:
1. Search for songs (read permission)
2. Create/delete playlists (write permission)

Both permissions are needed for the transfer to work.

### Step 3: Run the Transfer Script

Once authentication is working, run the main script:

```bash
python spotify-to-youtube-music.py
```

The script will:
1. Open your browser to authenticate with Spotify
2. Retrieve your Spotify playlists
3. Let you select which playlist to transfer
4. Create a new YouTube Music playlist with the same name
5. Search for and add each track, one by one

## Common Issues and Solutions

### Spotify Authentication Issues

1. **"Invalid client" error**:
   - Double-check that you've entered the correct Client ID and Client Secret
   - Make sure the redirect URI is exactly `http://localhost:8888/callback` (no trailing slash)

2. **Browser doesn't open for authentication**:
   - Manually open the Spotify authorization URL provided in the console
   - If the redirect fails, check that port 8888 isn't being used by another application

### YouTube Music Authentication Issues

1. **"Unauthorized" Error When Creating Playlists**:
   - Your authentication cookies might be expired. Run `youtube_auth_helper.py` again
   - Make sure you're including ALL cookies, not just the ones mentioned
   - Check that you've copied the full Authorization header

2. **Rate Limit Errors**:
   - YouTube Music limits how many requests you can make
   - The script includes pauses between requests, but for large playlists, YouTube might still rate-limit you
   - If this happens, wait a few hours before trying again

3. **"NoneType is not subscriptable" Error**:
   - This usually indicates an authentication problem
   - Run `test_auth.py` to diagnose issues with your authentication file

## Configuration Options

The script allows some customization:

1. **Playlist Privacy**: By default, created playlists are `PRIVATE`. If you want to change this, modify the `privacy_status` parameter in the `create_playlist` function to `"PUBLIC"` or `"UNLISTED"`.

2. **Search Query Format**: The script searches for tracks using `"{track_name} {artists}"`. If you're getting poor matches, you can modify the `search_query` format in the `transfer_to_youtube_music` function.

## How It Works

1. **Spotify Authentication**: The script uses OAuth 2.0 to access your Spotify account. It only requests read access to your playlists.

2. **Playlist Retrieval**: Once authenticated, it fetches the list of your playlists and their tracks.

3. **YouTube Music Matching**: For each track in your Spotify playlist, the script searches YouTube Music and selects the best match.

4. **Playlist Creation**: The script creates a new playlist in your YouTube Music account and adds the matched tracks.

## Privacy and Security

- Your Spotify credentials are never stored; the OAuth flow is handled securely.
- Your YouTube Music authentication cookies are stored locally in `headers_auth.json` - treat this file like a password!
- The script only sends requests to Spotify and YouTube Music APIs.
- No data is sent to third parties or stored online.

## Technical Details

This tool uses:
- [ytmusicapi](https://github.com/sigma67/ytmusicapi) - For YouTube Music API access
- Spotify Web API - For accessing Spotify playlists

## Credits

Created by FR3T0T & Frederik T.

## Contributing

Contributions are welcome! If you encounter issues or have improvements, please open an issue or submit a pull request.