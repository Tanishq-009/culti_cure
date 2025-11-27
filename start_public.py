import subprocess
import sys
import time
import requests

def get_public_ip():
    try:
        response = requests.get('https://api.ipify.org', timeout=5)
        return response.text
    except:
        return "Could not determine public IP"

def start_with_tunnel():
    print("=" * 60)
    print("Starting CultiKure Disease Prediction App")
    print("=" * 60)
    print(f"\nLocal URL: http://localhost:5000")
    print(f"Local Network URL: http://0.0.0.0:5000")
    
    public_ip = get_public_ip()
    print(f"\nYour Public IP: {public_ip}")
    print("\nTo make it publicly accessible:")
    print("1. Make sure port 5000 is open in your firewall")
    print("2. Access via: http://" + public_ip + ":5000")
    print("\nOR use a tunneling service like:")
    print("- localhost.run (free, no signup): ssh -R 80:localhost:5000 serveo.net")
    print("- ngrok (requires free account): ngrok http 5000")
    print("\nApp is running! Press Ctrl+C to stop.")
    print("=" * 60)
    
    # Import and run the Flask app
    from app import app
    app.run(host='0.0.0.0', port=5000, debug=False)

if __name__ == '__main__':
    start_with_tunnel()




