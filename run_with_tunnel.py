import subprocess
import sys
import re
import time
import os
import threading

def run_app_with_tunnel():
    """Run the Flask app and create a public tunnel"""
    
    print("=" * 70)
    print("CultiKure Disease Prediction App - Starting with Public Tunnel")
    print("=" * 70)
    
    # Start Flask app in background thread
    def start_flask():
        from app import app
        app.run(host='0.0.0.0', port=5000, debug=False)
    
    flask_thread = threading.Thread(target=start_flask, daemon=True)
    flask_thread.start()
    time.sleep(2)  # Wait for Flask to start
    
    # Check if cloudflared exists
    cloudflared_path = "./cloudflared.exe"
    if not os.path.exists(cloudflared_path):
        print(f"\n❌ {cloudflared_path} not found!")
        print("\n📱 Local access only:")
        print("   http://localhost:5000")
        print("\n🌐 To get a public URL:")
        print("   1. Download cloudflared from: https://github.com/cloudflare/cloudflared/releases")
        print("   2. Place cloudflared.exe in this directory")
        print("   3. Run this script again")
        print("\n   OR use ngrok (requires free account):")
        print("   - Install: pip install pyngrok")
        print("   - Sign up: https://dashboard.ngrok.com/signup")
        print("   - Run: ngrok http 5000")
        print("\n" + "=" * 70)
        print("✅ Flask app is running at: http://localhost:5000")
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print("\n\nApp stopped.")
        return
    
    # Start cloudflared tunnel
    print("\n🚀 Starting Cloudflared tunnel...")
    print("   Waiting for public URL (this may take 10-15 seconds)...")
    print("-" * 70)
    
    try:
        process = subprocess.Popen(
            [cloudflared_path, "tunnel", "--url", "http://localhost:5000"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            bufsize=1
        )
        
        public_url = None
        max_wait = 20  # Wait up to 20 seconds
        elapsed = 0
        
        # Read stderr (cloudflared outputs URL to stderr)
        import select
        import threading
        
        def read_output():
            nonlocal public_url
            for line in process.stderr:
                line = line.strip()
                if line:
                    print(f"[Cloudflared] {line}")
                    # Look for the URL
                    url_match = re.search(r'https://[a-zA-Z0-9-]+\.trycloudflare\.com', line)
                    if url_match and not public_url:
                        public_url = url_match.group(0)
                        print("\n" + "=" * 70)
                        print(f"✅ SUCCESS! Public URL created!")
                        print("=" * 70)
                        print(f"\n🌐 PUBLIC URL: {public_url}")
                        print(f"📱 Local URL: http://localhost:5000")
                        print("\n" + "=" * 70)
                        print("✅ Your app is now publicly accessible!")
                        print("   Share this URL with anyone to access your app.")
                        print("=" * 70)
        
        # Start reading output in a thread
        output_thread = threading.Thread(target=read_output, daemon=True)
        output_thread.start()
        
        # Wait a bit for the URL
        time.sleep(15)
        
        if not public_url:
            # Try reading from stdout as well
            try:
                for line in process.stdout:
                    line = line.strip()
                    if line:
                        url_match = re.search(r'https://[a-zA-Z0-9-]+\.trycloudflare\.com', line)
                        if url_match:
                            public_url = url_match.group(0)
                            print("\n" + "=" * 70)
                            print(f"✅ PUBLIC URL: {public_url}")
                            print("=" * 70)
                            break
            except:
                pass
        
        if public_url:
            print(f"\n✅ Tunnel is active! Public URL: {public_url}")
            print("Press Ctrl+C to stop the app and tunnel.")
        else:
            print("\n⚠️  Could not automatically detect public URL.")
            print("Check the cloudflared output above for the URL.")
            print("Or access locally at: http://localhost:5000")
        
        # Keep the process running
        process.wait()
        
    except Exception as e:
        print(f"\n❌ Error creating tunnel: {e}")
        print("\n📱 Running app locally only at: http://localhost:5000")
        from app import app
        app.run(host='0.0.0.0', port=5000, debug=False)

if __name__ == '__main__':
    run_app_with_tunnel()




