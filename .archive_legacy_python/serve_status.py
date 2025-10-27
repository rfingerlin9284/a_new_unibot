#!/usr/bin/env python3
"""
RICK System Status Server
Simple HTTP server for status.html with optional Flask API endpoints.
Port: 8080 (default)
"""

import http.server
import socketserver
import os
import sys
from pathlib import Path

PORT = int(os.getenv("STATUS_PORT", "8080"))
DIRECTORY = Path(__file__).parent  # Serve from project root


class StatusHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    """Custom handler for status page serving."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(DIRECTORY), **kwargs)

    def log_message(self, format, *args):
        """Override to provide cleaner logging."""
        sys.stderr.write(f"[{self.log_date_time_string()}] {format % args}\n")

    def end_headers(self):
        """Add CORS headers for local development."""
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, OPTIONS")
        self.send_header("Cache-Control", "no-cache, no-store, must-revalidate")
        super().end_headers()


def main():
    """Start the status server."""
    handler = StatusHTTPRequestHandler
    
    with socketserver.TCPServer(("0.0.0.0", PORT), handler) as httpd:
        print(f"🟢 RICK Status Server running on http://localhost:{PORT}")
        print(f"📊 Serving status.html from: {DIRECTORY}")
        print(f"🔄 Auto-refresh: 15s")
        print(f"🛑 Press Ctrl+C to stop\n")
        
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n\n🛑 Status server stopped")
            sys.exit(0)


if __name__ == "__main__":
    main()
