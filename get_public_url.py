import subprocess
import sys
import re
import time
import threading

def get_cloudflared_url():
    """Run cloudflared and extract the public URL"""
    try:
        print("Starting Cloudflared tunnel...")
        print("Waiting for public URL...")
        print("=" * 60)
        
        # Run cloudflared
        process = subprocess.Popen(
            ["./cloudflared.exe", "tunnel", "--url", "http://localhost:5000"],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=1
        )
        
        url_found = False
        for line in process.stdout:
            print(line.strip())
            # Cloudflared outputs the URL in a specific format
            if "https://" in line and ".trycloudflare.com" in line:
                url_match = re.search(r'https://[a-z0-9-]+\.trycloudflare\.com', line)
                if url_match:
                    public_url = url_match.group(0)
                    print("\n" + "=" * 60)
                    print(f"✅ PUBLIC URL: {public_url}")
                    print("=" * 60)
                    print(f"\nYour app is now accessible at: {public_url}")
                    print("Share this URL with anyone to access your app!")
                    print("\nPress Ctrl+C to stop the tunnel.")
                    print("=" * 60)
                    url_found = True
            elif "https://" in line:
                # Try to find any https URL
                url_match = re.search(r'https://[^\s]+', line)
                if url_match:
                    public_url = url_match.group(0)
                    print("\n" + "=" * 60)
                    print(f"✅ PUBLIC URL: {public_url}")
                    print("=" * 60)
                    url_found = True
        
        process.wait()
        
    except FileNotFoundError:
        print("cloudflared.exe not found. Please make sure it's in the current directory.")
        print("\nAlternative: The app is running at http://localhost:5000")
        print("You can access it locally or set up port forwarding.")
    except Exception as e:
        print(f"Error: {e}")
        print("\nThe app is running at http://localhost:5000")

if __name__ == '__main__':
    get_cloudflared_url()




