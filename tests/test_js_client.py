import http.server
import socketserver
import threading
import subprocess
import textwrap
from pathlib import Path
import shutil
import pytest


def test_js_client_rejects_on_error():
    if shutil.which("node") is None:
        pytest.skip("node executable not found")
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
                    console.log('no-error');
                except Exception as e:
                    console.log('err:' + String(e));
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


def _run_node(script: str, root: Path):
    return subprocess.run(["node", "-e", script], capture_output=True, text=True, cwd=root)


def test_js_client_streaming():
    if shutil.which("node") is None:
        pytest.skip("node executable not found")

    class Handler(http.server.BaseHTTPRequestHandler):
        def do_POST(self):
            self.send_response(200)
            self.send_header("content-type", "text/event-stream")
            self.end_headers()
            self.wfile.write(b"data: A\n\n")
            self.wfile.write(b"data: B\n\n")

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
                import {{ chatStream }} from './sdk/js/gptfrenzy-client.js';
                let out = '';
                for await (const t of chatStream('http://127.0.0.1:{port}', 'x', 'y')) {{
                    out += t;
                }}
                console.log('out:' + out);
                """
            )
            root = Path(__file__).resolve().parents[1]
            result = _run_node(script, root)
            assert "out:AB" in result.stdout
        finally:
            server.shutdown()
            thread.join()


def test_js_client_stream_error():
    if shutil.which("node") is None:
        pytest.skip("node executable not found")

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
                import {{ chatStream }} from './sdk/js/gptfrenzy-client.js';
                try {{
                    for await (const _ of chatStream('http://127.0.0.1:{port}', 'x', 'y')) {{}}
                    console.log('no-error');
                }} catch (e) {{
                    console.log('err:' + String(e));
                }}
                """
            )
            root = Path(__file__).resolve().parents[1]
            result = _run_node(script, root)
            assert "err:HTTP 500" in result.stdout
        finally:
            server.shutdown()
            thread.join()
