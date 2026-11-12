import socket
import threading
import time
import sys
import webview
from waitress import create_server
from app import create_app

def find_free_port() -> int:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(('127.0.0.1', 0))
        return s.getsockname()[1]

class DesktopServer:
    def __init__(self, app, port: int):
        self.server = create_server(app, host='127.0.0.1', port=port, threads=6)
        self.thread = threading.Thread(target=self.server.run, daemon=True)

    def start(self):
        self.thread.start()

    def stop(self):
        self.server.close()

def main():
    app = create_app()
    port = find_free_port()
    server = DesktopServer(app, port)
    server.start()

    time.sleep(0.3)

    webview.create_window(
        title='AgriPulse — Smarter Livestock Management',
        url=f'http://127.0.0.1:{port}',
        width=1366,
        height=840,
        min_size=(1024, 680)
    )
    webview.start()
    server.stop()
    sys.exit(0)

if __name__ == '__main__':
    main()