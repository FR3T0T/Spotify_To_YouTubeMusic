# Spotify to YouTube Music Playlist Transfer

This tool allows you to transfer your Spotify playlists to YouTube Music automatically. It uses the Spotify and YouTube Music APIs to fetch your playlists from Spotify and recreate them on YouTube Music.

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

## Files Included

- `spotify-to-youtube-music.py` - The main script for transferring playlists
- `youtube_auth_helper.py` - Helper script for YouTube Music authentication
- `test_auth.py` - Simple script to test if your authentication is working

## Usage

### Step 1: Set Up YouTube Music Authentication

First, you need to create an authentication file for YouTube Music:

```bash
python youtube_auth_helper.py
```

Follow the on-screen instructions to:
1. Log into YouTube Music in your browser
2. Extract cookies and authorization headers from browser developer tools
3. Create a working `headers_auth.json` file

### Step 2: Run the Transfer Script

Once you have a working authentication file, run the main script:

```bash
python spotify-to-youtube-music.py
```

The script will:
1. Open your browser to authenticate with Spotify
2. Show your Spotify playlists
3. Let you select which playlist to transfer
4. Create a new YouTube Music playlist
5. Transfer tracks one by one

## Troubleshooting

### Authentication Issues

If you encounter authentication errors:

1. **YouTube Music Authentication Fails**:
   - Make sure you're logged into YouTube Music in your browser
   - Follow the steps in `youtube_auth_helper.py` carefully
   - Try running `test_auth.py` to verify your authentication works

2. **"Unauthorized" Error When Creating Playlists**:
   - Your authentication file may be missing required cookies
   - Run `youtube_auth_helper.py` again and make sure to copy the entire cookie string
   - Make sure to include the full Authorization header

3. **Spotify Authentication Issues**:
   - The script handles Spotify authentication automatically
   - Make sure your browser can open and you can log into Spotify

## How It Works

1. The script uses Spotify's OAuth to access your playlists
2. It fetches the tracks in your selected playlist
3. For each track, it searches YouTube Music for a matching song
4. It adds the found songs to a new YouTube Music playlist

## Technical Details

The authentication with YouTube Music uses a combination of cookies and an authorization token from your browser. The tool does not store your password or login credentials; it only uses the session tokens from your browser.

## Privacy and Security

- Your authentication details are stored locally in the `headers_auth.json` file
- No data is sent to third-party services other than Spotify and YouTube Music APIs
- The tool doesn't store or share your playlists or usage data

## Credits

This tool uses:
- [ytmusicapi](https://github.com/sigma67/ytmusicapi) - For YouTube Music API access
- Spotify Web API - For accessing Spotify playlists