import socket
import threading
import time
import webbrowser
from waitress import serve
from app import create_app

app = create_app()

def get_local_ip() -> str:
    """Finds the computer's local Wi-Fi / Hotspot IP address for phone access."""
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            s.connect(("8.8.8.8", 80))
            return s.getsockname()[0]
    except Exception:
        return "127.0.0.1"

def open_browser(port: int):
    time.sleep(1.0)
    webbrowser.open(f"http://127.0.0.1:{port}")

if __name__ == "__main__":
    PORT = 5000
    local_ip = get_local_ip()

    print("=" * 62)
    print("  AGRIPULSE — SMARTER LIVESTOCK MANAGEMENT")
    print("=" * 62)
    print(f"  * Laptop Browser URL : http://127.0.0.1:{PORT}")
    print(f"  * Phone Browser URL  : http://{local_ip}:{PORT} (Same Wi-Fi/Hotspot)")
    print("=" * 62)

    threading.Thread(target=open_browser, args=(PORT,), daemon=True).start()
    serve(app, host="0.0.0.0", port=PORT, threads=6)