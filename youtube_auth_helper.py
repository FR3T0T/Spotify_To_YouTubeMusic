import os
import sys
import json
import time

# Check for ytmusicapi
try:
    from ytmusicapi import YTMusic
except ImportError:
    print("Error: ytmusicapi is not installed. Install it using: pip install ytmusicapi")
    sys.exit(1)

print("=" * 60)
print("YouTube Music Authentication Helper")
print("=" * 60)

def create_headers_file():
    """Create a headers_auth.json file with the required fields."""
    print("\nCreating an authentication file for YouTube Music...")
    
    # Get required cookie values
    print("\nPlease follow these steps to get your cookies and authorization:")
    print("1. Open YouTube Music in your browser (music.youtube.com)")
    print("2. Make sure you're logged in")
    print("3. Open developer tools (F12 or right-click > Inspect)")
    print("4. Go to the Network tab")
    print("5. Refresh the page")
    print("6. Find any request to 'browse' or similar YouTube Music API requests")
    print("7. Click on the request and look in the 'Headers' tab")
    
    # Get cookie header
    print("\nFirst, I need you to copy the entire Cookie header value:")
    print("1. In the Request Headers section, find 'Cookie:'")
    print("2. Right-click on the Cookie value and select 'Copy value'")
    print("3. Paste the ENTIRE cookie string below")
    
    cookie_value = input("\nPaste the complete Cookie header value: ").strip()
    
    # Get authorization header
    print("\nNow I need the Authorization header:")
    print("1. Still in the Headers tab, find 'Authorization:'")
    print("2. Copy the entire value (starts with 'SAPISIDHASH')")
    
    auth_value = input("\nPaste the complete Authorization header value: ").strip()
    
    # Create the headers object
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36",
        "Accept": "*/*",
        "Accept-Language": "en-US,en;q=0.9",
        "Content-Type": "application/json",
        "X-Goog-AuthUser": "0",
        "x-origin": "https://music.youtube.com",
        "Cookie": cookie_value,
        "Authorization": auth_value
    }
    
    # Save to file
    with open("headers_auth.json", "w") as f:
        json.dump(headers, f, indent=2)
    
    print("\n✓ Headers saved to headers_auth.json")
    return True

def test_auth():
    """Test if the authentication file works for both read and write operations."""
    print("\nTesting authentication...")
    
    try:
        ytmusic = YTMusic("headers_auth.json")
        
        # Test 1: Basic search (read operation)
        print("\nTest 1: Basic search...")
        search_results = ytmusic.search("test", filter="songs", limit=1)
        
        if search_results:
            print("✓ Search test successful!")
            print(f"  Found song: {search_results[0].get('title', 'Unknown')}")
        else:
            print("× Search test failed: No results returned.")
            return False
        
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
            print("\nAuthentication has issues with write operations. You need full permissions.")
            return False
            
        return True
    except Exception as e:
        print(f"× Authentication test failed: {str(e)}")
        return False

def main():
    """Main function to handle YouTube Music authentication."""
    
    print("\nThis script will help you set up authentication for YouTube Music.")
    
    # Check for existing auth file
    if os.path.exists("headers_auth.json"):
        print("\nFound existing authentication file: headers_auth.json")
        print("Testing if it works...")
        
        if test_auth():
            print("\n✓ Existing authentication is working! You can now run the main script.")
            return
        else:
            print("\n× Existing authentication doesn't work. Let's create a new one.")
    
    # Create and test new auth file
    if create_headers_file():
        if test_auth():
            print("\n✓ Authentication is working! You can now run the main script.")
            return
        else:
            print("\n× Authentication test failed after creating new headers file.")
            print("Please make sure you copied the correct values and try again.")
    
    print("\n× Authentication setup failed.")
    print("Please make sure you're properly logged into YouTube Music in your browser")
    print("and that you're following the instructions carefully.")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nOperation cancelled by user")
        sys.exit(0)
    except Exception as e:
        print(f"\nUnexpected error: {str(e)}")
        sys.exit(1)