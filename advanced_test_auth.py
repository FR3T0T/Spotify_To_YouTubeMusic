from ytmusicapi import YTMusic
import sys
import time
import json

print("=" * 60)
print("Advanced YouTube Music Authentication Test")
print("=" * 60)

try:
    # Initialize YTMusic with the headers file
    print("\nTesting authentication with headers_auth.json...")
    ytmusic = YTMusic("headers_auth.json")
    
    # Test 1: Basic search (simple operation)
    print("\nTest 1: Basic search...")
    search_results = ytmusic.search("test", filter="songs", limit=1)
    
    if search_results:
        print("✓ Search test successful!")
        print(f"  Found song: {search_results[0].get('title', 'Unknown')}")
    else:
        print("× Search test failed: No results returned.")
        sys.exit(1)
    
    # Test 2: Check if we can access user's library (requires more permissions)
    print("\nTest 2: Accessing user library...")
    try:
        library = ytmusic.get_library_playlists(limit=1)
        print("✓ Library access test successful!")
        if library:
            print(f"  Found {len(library)} playlists in library")
        else:
            print("  Library is empty or not accessible")
    except Exception as e:
        print(f"× Library access test failed: {str(e)}")
    
    # Test 3: Create a test playlist
    print("\nTest 3: Creating a test playlist...")
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
        
    print("\nSummary of headers in headers_auth.json:")
    try:
        with open("headers_auth.json", "r") as f:
            headers = json.load(f)
            print(f"- User-Agent: {headers.get('User-Agent', 'Missing')}")
            print(f"- Content-Type: {headers.get('Content-Type', 'Missing')}")
            print(f"- Authorization: {'Present' if headers.get('Authorization') else 'Missing'}")
            
            # Count cookies
            if 'Cookie' in headers:
                cookie_count = headers['Cookie'].count(';') + 1
                print(f"- Cookie: {cookie_count} cookies present")
            else:
                print("- Cookie: Missing")
    except Exception as e:
        print(f"Error reading headers_auth.json: {str(e)}")
    
except Exception as e:
    print(f"× Authentication failed: {str(e)}")
    sys.exit(1)

print("\n" + "=" * 60)