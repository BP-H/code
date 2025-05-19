import http.server
import socketserver
import threading
import subprocess
import textwrap
from pathlib import Path


def test_js_client_rejects_on_error():
    class Handler(http.server.BaseHTTPRequestHandler):
        def do_POST(self):
            self.send_response(500)
            self.end_headers()
            self.wfile.write(b"{}")

        def log_message(self, *args):
            pass

    with socketserver.TCPServer(("127.0.0.1", 0), Handler) as server:
        thread = threading.Thread(target=server.serve_forever)
        thread.daemon = True
        thread.start()
        try:
            port = server.server_address[1]
            script = textwrap.dedent(
                f"""
                import {{ chat }} from './sdk/js/gptfrenzy-client.js';
                try:
                    await chat('http://127.0.0.1:{port}', 'x', 'y');
                    print('no-error')
                except Exception as e:
                    print('err:' + str(e))
                """
            )
            root = Path(__file__).resolve().parents[1]
            result = subprocess.run(
                ["node", "-e", script], capture_output=True, text=True, cwd=root
            )
            assert "err:HTTP 500" in result.stdout
        finally:
            server.shutdown()
            thread.join()
