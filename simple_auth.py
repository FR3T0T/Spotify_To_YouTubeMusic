import os
import sys
import json

# Check for ytmusicapi
try:
    from ytmusicapi import YTMusic
except ImportError:
    print("Error: ytmusicapi is not installed. Install it using: pip install ytmusicapi")
    sys.exit(1)

print("=" * 60)
print("Simplified YouTube Music Authentication Helper")
print("=" * 60)

def create_raw_file():
    """
    Create a simple text file with raw request headers that YTMusic can process.
    This method is more reliable than trying to format the headers ourselves.
    """
    print("\nThis script will create a raw headers file for YouTube Music authentication.")
    print("\nPlease follow these steps:")
    print("1. Open YouTube Music in your browser (music.youtube.com)")
    print("2. Make sure you're logged in")
    print("3. Open developer tools (F12 or right-click > Inspect)")
    print("4. Go to the Network tab")
    print("5. Refresh the page")
    print("6. Find any request to 'browse' or similar")
    print("7. Right-click the request > Copy > Copy as cURL (bash)")
    print("8. Create a new text file named 'headers_raw.txt'")
    print("9. Paste the cURL command into this file and save it")
    
    input("\nPress Enter when you've created the headers_raw.txt file...")
    
    if not os.path.exists("headers_raw.txt"):
        print("× Error: headers_raw.txt file not found in the current directory.")
        return False
    
    try:
        # Run the ytmusicapi setup_from_file method
        YTMusic.setup_from_file("headers_raw.txt", "headers_auth.json")
        print("✓ Successfully created headers_auth.json from your file!")
        return True
    except Exception as e:
        print(f"× Error creating headers file: {str(e)}")
        return False

def create_manual_headers():
    """Create a headers_auth.json file with manually entered values."""
    print("\nCreating a manual authentication file for YouTube Music...")
    
    print("\nI'll need you to paste the entire Cookie header value.")
    print("1. In Chrome DevTools Network tab, click on any music.youtube.com request")
    print("2. In the Headers tab, find 'Cookie:' under Request Headers")
    print("3. Right-click on the Cookie value and select 'Copy value'")
    print("4. Paste the ENTIRE cookie string below")
    
    cookie_value = input("\nPaste the complete Cookie header value: ").strip()
    
    print("\nNow I need the Authorization header.")
    print("1. In the same Headers section, find 'Authorization:'")
    print("2. Copy the entire value (starts with SAPISIDHASH)")
    
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
    """Test if the authentication file works."""
    print("\nTesting authentication...")
    
    try:
        ytmusic = YTMusic("headers_auth.json")
        
        # Try a simple API call
        print("Making a test API call...")
        search_results = ytmusic.search("test", filter="songs", limit=1)
        
        if search_results:
            print("✓ Authentication successful!")
            return True
        else:
            print("× Authentication failed: No results returned")
            return False
    except Exception as e:
        print(f"× Authentication test failed: {str(e)}")
        return False

def main():
    """Main function to handle YouTube Music authentication."""
    
    print("\nThis script will help you set up authentication for YouTube Music.")
    
    # Try to create headers file using raw curl method
    print("\nLet's try the 'raw headers' method first (Option 1)...")
    if create_raw_file() and test_auth():
        print("\n✓ Authentication is working! You can now run the main script.")
        return
    
    # If that failed, try manual method
    print("\nLet's try the 'manual headers' method (Option 2)...")
    if create_manual_headers() and test_auth():
        print("\n✓ Manual authentication is working! You can now run the main script.")
        return
    
    print("\n× Both authentication methods failed.")
    print("\nAlternative solution:")
    print("1. Try installing a brand new version of ytmusicapi:")
    print("   pip install --upgrade ytmusicapi")
    print("\n2. Instead of using the auth methods in this script, try:")
    print("   - Create a file named 'browser.json' with this content:")
    print('   {"browser": "chrome"}')
    print("   - Run this command: ytmusicapi setup --browser browser.json")
    print("   - This will create a headers_auth.json file you can use")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nOperation cancelled by user")
        sys.exit(0)
    except Exception as e:
        print(f"\nUnexpected error: {str(e)}")
        sys.exit(1)