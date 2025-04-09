import json
import os
from ytmusicapi import YTMusic

print("=" * 60)
print("Minimal YouTube Music Authentication")
print("=" * 60)

# Create a headers_auth.json file directly
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36",
    "Accept": "*/*",
    "Accept-Language": "en-US,en;q=0.9",
    "Content-Type": "application/json",
    "X-Goog-AuthUser": "0",
    "x-origin": "https://music.youtube.com"
}

print("\nPlease go to YouTube Music in your browser.")
print("Open DevTools (F12) > Application tab > Cookies > https://music.youtube.com")
print("\nFind and copy these cookie values:")

# Get the required cookies
headers["Cookie"] = ""

# These are the essential cookies
cookies = [
    "__Secure-3PAPISID",
    "__Secure-3PSID",
    "SAPISID"
]

for cookie in cookies:
    value = input(f"Enter the value for cookie '{cookie}': ").strip()
    headers["Cookie"] += f"{cookie}={value}; "

# Write the headers to a file
with open("headers_auth.json", "w") as f:
    json.dump(headers, f, indent=2)

print("\n✓ Created headers_auth.json file")

# Test the authentication
try:
    print("\nTesting authentication...")
    ytmusic = YTMusic("headers_auth.json")
    
    # Try a simple API call
    search_results = ytmusic.search("test", filter="songs", limit=1)
    
    if search_results:
        print("✓ Authentication successful!")
        print("\nYou can now run your Spotify to YouTube Music script.")
    else:
        print("× No results returned. Authentication might not be working correctly.")
except Exception as e:
    print(f"× Authentication test failed: {str(e)}")
    print("\nYou may need to:")
    print("1. Update ytmusicapi: pip install --upgrade ytmusicapi")
    print("2. Make sure you're logged into YouTube Music in your browser")
    print("3. Check that you copied the cookie values correctly")