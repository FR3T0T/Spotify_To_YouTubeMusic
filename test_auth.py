from ytmusicapi import YTMusic
import sys
import json
import time

print("=" * 60)
print("YouTube Music Authentication Test")
print("=" * 60)

try:
    # Initialize YTMusic with the headers file
    print("\nTesting authentication with headers_auth.json...")
    ytmusic = YTMusic("headers_auth.json")
    
    # Test 1: Basic search (read operation)
    print("\nTest 1: Basic search...")
    search_results = ytmusic.search("test", filter="songs", limit=1)
    
    if search_results:
        print("✓ Search test successful!")
        print(f"  Found song: {search_results[0].get('title', 'Unknown')}")
    else:
        print("× Search test failed: No results returned.")
        sys.exit(1)
    
    # Test 2: Create a test playlist (write operation)
    print("\nTest 2: Creating a test playlist...")
    try:
        playlist_name = f"Test Playlist {int(time.time())}"
        playlist_id = ytmusic.create_playlist(
            title=playlist_name,
            description="Test playlist for authentication check",
            privacy_status="PRIVATE"
        )
        print(f"✓ Playlist creation test successful!")
        print(f"  Created playlist with ID: {playlist_id}")
        
        # Try to delete the test playlist
        print("\nCleaning up: Deleting test playlist...")
        try:
            ytmusic.delete_playlist(playlist_id)
            print("✓ Successfully deleted test playlist")
        except Exception as e:
            print(f"× Could not delete test playlist: {str(e)}")
    
    except Exception as e:
        print(f"× Playlist creation test failed: {str(e)}")
        print("\nAuthentication has issues with write operations.")
        sys.exit(1)
        
    print("\nSummary of headers in headers_auth.json:")
    try:
        with open("headers_auth.json", "r") as f:
            headers = json.load(f)
            print(f"- User-Agent: {'Present' if 'User-Agent' in headers else 'Missing'}")
            print(f"- Content-Type: {'Present' if 'Content-Type' in headers else 'Missing'}")
            print(f"- Authorization: {'Present' if 'Authorization' in headers else 'Missing'}")
            
            # Count cookies
            if 'Cookie' in headers:
                cookie_count = headers['Cookie'].count(';') + 1
                print(f"- Cookie: {cookie_count} cookies present")
                
                # Check for essential cookies
                essential_cookies = ['__Secure-3PAPISID', '__Secure-3PSID', 'SAPISID']
                for cookie in essential_cookies:
                    if cookie in headers['Cookie']:
                        print(f"  ✓ {cookie} cookie present")
                    else:
                        print(f"  × {cookie} cookie missing")
            else:
                print("- Cookie: Missing")
    except Exception as e:
        print(f"Error reading headers_auth.json: {str(e)}")
    
    print("\n✅ AUTHENTICATION IS WORKING CORRECTLY!")
    print("You can now run the main script: python spotify-to-youtube-music.py")
    
except Exception as e:
    print(f"× Authentication failed: {str(e)}")
    print("\nPlease run the authentication helper script:")
    print("python youtube_auth_helper.py")
    sys.exit(1)

print("=" * 60)