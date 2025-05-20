import http.server
import socketserver
import threading
import subprocess
import textwrap
from pathlib import Path
import shutil
import tempfile
import pytest


def _dotnet():
    return shutil.which("dotnet")


@pytest.mark.skipif(_dotnet() is None, reason="dotnet executable not found")
def test_csharp_client_streaming():
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
            tmp = Path(tempfile.mkdtemp())
            subprocess.check_call([
                _dotnet(),
                "new",
                "console",
                "--output",
                str(tmp),
            ])
            subprocess.check_call([
                _dotnet(),
                "add",
                str(tmp),
                "package",
                "Newtonsoft.Json",
            ])
            root = Path(__file__).resolve().parents[1]
            (tmp / "GptFrenzyClient.cs").write_text(Path(root / "sdk/csharp/GptFrenzyClient.cs").read_text())
            (tmp / "Program.cs").write_text(textwrap.dedent(f"""
using System;
using System.Threading.Tasks;
class Program {{
    static async Task Main() {{
        var c = new GptFrenzyClient("http://127.0.0.1:{port}");
        string res = "";
        await foreach (var t in c.ChatStream("x","y")) {{ res += t; }}
        Console.WriteLine("out:" + res);
    }}
}}
"""))
            result = subprocess.run([_dotnet(), "run", "--project", str(tmp)], capture_output=True, text=True)
            assert "out:AB" in result.stdout
        finally:
            server.shutdown()
            thread.join()


@pytest.mark.skipif(_dotnet() is None, reason="dotnet executable not found")
def test_csharp_client_stream_error():
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
            tmp = Path(tempfile.mkdtemp())
            subprocess.check_call([
                _dotnet(),
                "new",
                "console",
                "--output",
                str(tmp),
            ])
            subprocess.check_call([
                _dotnet(),
                "add",
                str(tmp),
                "package",
                "Newtonsoft.Json",
            ])
            root = Path(__file__).resolve().parents[1]
            (tmp / "GptFrenzyClient.cs").write_text(Path(root / "sdk/csharp/GptFrenzyClient.cs").read_text())
            (tmp / "Program.cs").write_text(textwrap.dedent(f"""
using System;
using System.Threading.Tasks;
class Program {{
    static async Task Main() {{
        try {{
            var c = new GptFrenzyClient("http://127.0.0.1:{port}");
            await foreach (var _ in c.ChatStream("x","y")) {{ }}
            Console.WriteLine("no-error");
        }} catch (Exception e) {{
            Console.WriteLine("err:" + e.Message);
        }}
    }}
}}
"""))
            result = subprocess.run([_dotnet(), "run", "--project", str(tmp)], capture_output=True, text=True)
            assert "err:" in result.stdout
        finally:
            server.shutdown()
            thread.join()

