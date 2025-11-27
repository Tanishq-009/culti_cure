import subprocess
import sys
import threading
import time

def create_localhost_run_tunnel():
    """Create a tunnel using localhost.run via SSH"""
    try:
        print("Creating public tunnel via localhost.run...")
        print("This will create a public URL for your app.")
        print("\nTunnel URL will be displayed below...")
        print("=" * 60)
        
        # Use SSH to create tunnel to localhost.run
        # Format: ssh -R 80:localhost:5000 serveo.net
        cmd = ['ssh', '-o', 'StrictHostKeyChecking=no', '-R', '80:localhost:5000', 'serveo.net']
        
        process = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=1
        )
        
        # Read output in real-time
        for line in process.stdout:
            print(line.strip())
            if 'Forwarding' in line or 'http' in line.lower():
                print(f"\n✅ Public URL found: {line.strip()}")
        
        process.wait()
        
    except FileNotFoundError:
        print("SSH not found. Trying alternative method...")
        print("\nPlease use one of these methods to create a public URL:")
        print("1. Install Cloudflared: https://github.com/cloudflare/cloudflared/releases")
        print("   Then run: cloudflared tunnel --url http://localhost:5000")
        print("\n2. Use ngrok (requires free account):")
        print("   - Sign up at: https://dashboard.ngrok.com/signup")
        print("   - Install: pip install pyngrok")
        print("   - Run: ngrok http 5000")
        print("\n3. Use localhost.run (if SSH is available):")
        print("   ssh -R 80:localhost:5000 serveo.net")
        
    except Exception as e:
        print(f"Error creating tunnel: {e}")
        print("\nThe app is running locally at: http://localhost:5000")
        print("To make it public, use one of the tunneling services mentioned above.")

if __name__ == '__main__':
    create_localhost_run_tunnel()




