import http.server
import socketserver
import threading
import pytest

from sdk.python import gptfrenzy_client as gfc


class _BaseHandler(http.server.BaseHTTPRequestHandler):
    def log_message(self, *args):
        pass


def _serve(handler_cls):
    return socketserver.TCPServer(("127.0.0.1", 0), handler_cls)


def test_python_client_streaming():
    class Handler(_BaseHandler):
        def do_POST(self):
            self.send_response(200)
            self.send_header("content-type", "text/event-stream")
            self.end_headers()
            self.wfile.write(b"data: A\n\n")
            self.wfile.write(b"data: B\n\n")

    with _serve(Handler) as server:
        thread = threading.Thread(target=server.serve_forever)
        thread.daemon = True
        thread.start()
        try:
            port = server.server_address[1]
            c = gfc.GPTFrenzyClient(f"http://127.0.0.1:{port}")
            out = "".join(c.chat_stream("x", "y"))
            assert out == "AB"
        finally:
            server.shutdown()
            thread.join()


def test_python_client_stream_error():
    class Handler(_BaseHandler):
        def do_POST(self):
            self.send_response(500)
            self.end_headers()
            self.wfile.write(b"{}")

    with _serve(Handler) as server:
        thread = threading.Thread(target=server.serve_forever)
        thread.daemon = True
        thread.start()
        try:
            port = server.server_address[1]
            c = gfc.GPTFrenzyClient(f"http://127.0.0.1:{port}")
            with pytest.raises(Exception):
                list(c.chat_stream("x", "y"))
        finally:
            server.shutdown()
            thread.join()
