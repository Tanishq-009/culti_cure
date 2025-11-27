import subprocess
import threading
import time
import sys
import os

# Start Flask app in background thread
def run_flask():
    from app import app
    app.run(host='0.0.0.0', port=5000, debug=False)

# Start Flask in thread
flask_thread = threading.Thread(target=run_flask, daemon=True)
flask_thread.start()

# Wait for Flask to start
time.sleep(3)

# Try to create tunnel
try:
    from pyngrok import ngrok
    public_url = ngrok.connect(5000)
    print("\n" + "="*70)
    print("✅ APP IS RUNNING!")
    print("="*70)
    print(f"\n🌐 PUBLIC URL: {public_url}")
    print(f"📱 LOCAL URL: http://localhost:5000")
    print("\n" + "="*70)
    print("✅ Share the PUBLIC URL above to access from anywhere!")
    print("="*70)
    print("\nPress Ctrl+C to stop the app and tunnel.\n")
    
    # Keep running
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        ngrok.kill()
        print("\n\nApp stopped.")
except Exception as e:
    print(f"\n⚠️  Could not create tunnel: {e}")
    print(f"\n📱 App is running locally at: http://localhost:5000")
    print("   Access it from your browser or share via port forwarding.")
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n\nApp stopped.")

