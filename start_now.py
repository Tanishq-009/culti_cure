import subprocess
import threading
import time
import re
import os
import sys

print("=" * 70)
print("Starting CultiKure Disease Prediction App")
print("=" * 70)

# Start Flask in background
def run_flask():
    from app import app
    app.run(host='0.0.0.0', port=5000, debug=False)

flask_thread = threading.Thread(target=run_flask, daemon=True)
flask_thread.start()
print("\n✅ Flask app starting...")
time.sleep(3)

# Start cloudflared
if os.path.exists("./cloudflared.exe"):
    print("\n🚀 Creating public tunnel with Cloudflared...")
    print("   Please wait 10-15 seconds for the URL...\n")
    
    process = subprocess.Popen(
        ["./cloudflared.exe", "tunnel", "--url", "http://localhost:5000"],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        bufsize=1
    )
    
    url_found = False
    for line in process.stdout:
        line = line.strip()
        if line:
            print(line)
            # Look for URL
            match = re.search(r'https://[a-zA-Z0-9-]+\.trycloudflare\.com', line)
            if match and not url_found:
                public_url = match.group(0)
                print("\n" + "=" * 70)
                print("✅ SUCCESS! Your app is now accessible!")
                print("=" * 70)
                print(f"\n🌐 PUBLIC URL: {public_url}")
                print(f"📱 LOCAL URL: http://localhost:5000")
                print("\n" + "=" * 70)
                print("✅ Share the PUBLIC URL above to access from anywhere!")
                print("=" * 70)
                url_found = True
    
    if not url_found:
        print("\n⚠️  Could not detect URL automatically.")
        print("📱 App is running at: http://localhost:5000")
else:
    print("\n⚠️  cloudflared.exe not found")
    print("📱 App is running at: http://localhost:5000")
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n\nApp stopped.")

