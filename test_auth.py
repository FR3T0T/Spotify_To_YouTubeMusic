from ytmusicapi import YTMusic
import sys

print("Testing YouTube Music authentication...")

try:
    # Initialize YTMusic with the headers file
    ytmusic = YTMusic("headers_auth.json")
    
    # Make a simple test API call
    print("Making test API call...")
    search_results = ytmusic.search("test", filter="songs", limit=1)
    
    if search_results:
        print("✓ Authentication successful!")
        print(f"Found song: {search_results[0].get('title', 'Unknown')}")
    else:
        print("× No results returned. Authentication might be working but returned empty results.")
    
except Exception as e:
    print(f"× Authentication failed: {str(e)}")
    sys.exit(1)