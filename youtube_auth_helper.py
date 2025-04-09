import os
import sys
import json
import time
import subprocess

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
    """Create a headers_auth.json file with the minimum required fields."""
    print("\nCreating a simplified authentication file for YouTube Music...")
    
    # Get required cookie values
    print("\nPlease follow these steps to get your cookies and authorization:")
    print("1. Open YouTube Music in your browser (music.youtube.com)")
    print("2. Make sure you're logged in")
    print("3. Open developer tools (F12 or right-click > Inspect)")
    print("4. Go to the Application tab")
    print("5. In the left panel, expand 'Cookies' and select 'https://music.youtube.com'")
    print("6. Find these specific cookies and copy their values when prompted:")
    
    # Essential cookies
    cookies = {}
    
    # Get cookie values
    cookies['__Secure-3PAPISID'] = input("\nEnter the value of cookie '__Secure-3PAPISID': ").strip()
    cookies['__Secure-3PSID'] = input("Enter the value of cookie '__Secure-3PSID': ").strip()
    
    # Get authorization header
    print("\nNow we need the Authorization header:")
    print("1. Go to the Network tab in developer tools")
    print("2. Refresh the page and look for any request to 'browse' or 'next'")
    print("3. Click on the request and look in the 'Headers' tab")
    print("4. Find the 'Authorization' header under 'Request Headers'")
    print("   (It starts with 'SAPISIDHASH' or similar)")
    
    auth_header = input("\nEnter the Authorization header value: ").strip()
    
    # Create the headers object
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36",
        "Content-Type": "application/json",
        "Authorization": auth_header,
        "X-Goog-AuthUser": "0",
        "x-origin": "https://music.youtube.com"
    }
    
    # Add the cookie string
    cookie_str = ""
    for name, value in cookies.items():
        cookie_str += f"{name}={value}; "
    
    headers["Cookie"] = cookie_str
    
    # Save to file
    with open("headers_auth.json", "w") as f:
        json.dump(headers, f, indent=2)
    
    print("\n✓ Headers saved to headers_auth.json")
    return True

def try_oauth_standalone():
    """Try the standalone OAuth approach."""
    print("\nRunning the standalone OAuth setup...")
    
    try:
        # Prepare the command to run in a new process
        if os.name == 'nt':  # Windows
            cmd = ["python", "-m", "ytmusicapi", "oauth"]
        else:  # Unix/Mac
            cmd = ["python3", "-m", "ytmusicapi", "oauth"]
        
        # Run the command and capture output
        process = subprocess.run(cmd, check=True, text=True, capture_output=True)
        
        # Check if oauth.json was created
        if os.path.exists("oauth.json"):
            print("✓ Successfully created oauth.json!")
            return True
        else:
            print("× OAuth setup ran but oauth.json wasn't created.")
            print("Output: " + process.stdout)
            return False
    except subprocess.CalledProcessError as e:
        print(f"× Error running OAuth setup: {e}")
        print(f"Output: {e.stdout}")
        print(f"Error: {e.stderr}")
        return False
    except Exception as e:
        print(f"× Unexpected error: {str(e)}")
        return False

def test_auth(auth_file):
    """Test if the authentication file works."""
    print(f"\nTesting authentication using {auth_file}...")
    
    try:
        ytmusic = YTMusic(auth_file)
        
        # Try a simple API call
        print("Making a test API call...")
        home = ytmusic.get_library_playlists(limit=1)
        
        print(f"✓ Authentication successful using {auth_file}!")
        return True
    except Exception as e:
        print(f"× Authentication test failed: {str(e)}")
        return False

def main():
    """Main function to handle YouTube Music authentication."""
    
    print("\nThis script will help you set up authentication for YouTube Music.")
    
    # Check for existing auth files
    auth_files = []
    if os.path.exists("oauth.json"):
        auth_files.append("oauth.json")
    if os.path.exists("headers_auth.json"):
        auth_files.append("headers_auth.json")
    
    # Test existing auth files
    for auth_file in auth_files:
        print(f"\nFound existing authentication file: {auth_file}")
        if test_auth(auth_file):
            print(f"\n✓ You can now use {auth_file} with the main script!")
            return
        else:
            print(f"× Existing {auth_file} doesn't work, trying other methods...")
    
    # Try OAuth method first (most reliable)
    if try_oauth_standalone():
        if test_auth("oauth.json"):
            print("\n✓ OAuth authentication is working! You can now run the main script.")
            return
    
    # If OAuth failed, try the manual headers method
    print("\nTrying manual headers method...")
    if create_headers_file():
        if test_auth("headers_auth.json"):
            print("\n✓ Manual authentication is working! You can now run the main script.")
            return
    
    print("\n× All authentication methods failed.")
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