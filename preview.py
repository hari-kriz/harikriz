import http.server
import webbrowser
import threading

PORT = 8000
URL = f"http://localhost:{PORT}"

def open_browser():
    webbrowser.open(URL)

print(f"Starting server at {URL}")
print("Press Ctrl+C to stop\n")

threading.Timer(1, open_browser).start()
http.server.HTTPServer(("", PORT), http.server.SimpleHTTPRequestHandler).serve_forever()
