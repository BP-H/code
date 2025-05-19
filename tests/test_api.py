import sys
import types
import json

# Minimal httpx stub so FastAPI's TestClient can run without dependency.
if 'httpx' not in sys.modules:
    httpx = types.ModuleType('httpx')

    class URL:
        def __init__(self, url: str):
            if '://' in url:
                self.scheme, rest = url.split('://', 1)
            else:
                self.scheme, rest = 'http', url
            if '/' in rest:
                netloc, path_query = rest.split('/', 1)
                path_query = '/' + path_query
            else:
                netloc = rest
                path_query = '/'
            if '?' in path_query:
                path, query = path_query.split('?', 1)
            else:
                path, query = path_query, ''
            self.netloc = netloc.encode()
            self.path = path
            self.raw_path = path.encode()
            self.query = query.encode()

    class Request:
        def __init__(self, method: str, url: str, headers=None, content: bytes = b''):
            self.method = method
            self.url = URL(url)
            self.headers = headers or {}
            self._content = content

        def read(self) -> bytes:
            return self._content

    class ByteStream:
        def __init__(self, data: bytes):
            self._data = data

        def read(self) -> bytes:
            return self._data

    class Response:
        def __init__(self, status_code=200, headers=None, stream=None, request=None):
            self.status_code = status_code
            self.headers = {k: v for k, v in (headers or [])}
            if hasattr(stream, 'read'):
                self._content = stream.read()
            else:
                self._content = stream or b''
            self.request = request

        @property
        def text(self) -> str:
            return self._content.decode()

        def json(self):
            return json.loads(self.text)

    class BaseTransport:
        pass

    class Client:
        def __init__(self, *, app=None, base_url='', headers=None, transport=None, follow_redirects=True, cookies=None):
            self.base_url = base_url
            self.headers = headers or {}
            self._transport = transport

        def request(self, method, url, *, content=None, json=None, headers=None, **kwargs):
            if not url.startswith('http'):
                url = self.base_url.rstrip('/') + url
            hdrs = self.headers.copy()
            if headers:
                hdrs.update(headers)
            if json is not None:
                content = __import__('json').dumps(json).encode()
                hdrs.setdefault('content-type', 'application/json')
            if isinstance(content, str):
                content = content.encode()
            content = content or b''
            req = Request(method, url, hdrs, content)
            return self._transport.handle_request(req)

        def get(self, url, **kw):
            return self.request('GET', url, **kw)

        def post(self, url, **kw):
            return self.request('POST', url, **kw)

        def __enter__(self):
            return self

        def __exit__(self, *args):
            pass

    httpx.URL = URL
    httpx.Request = Request
    httpx.Response = Response
    httpx.ByteStream = ByteStream
    httpx.BaseTransport = BaseTransport
    httpx.Client = Client
    httpx._client = types.SimpleNamespace(
        USE_CLIENT_DEFAULT=None,
        CookieTypes=None,
        TimeoutTypes=None,
        UseClientDefault=None,
    )
    httpx._types = types.SimpleNamespace(
        URLTypes=str,
        HeaderTypes=dict,
        CookieTypes=dict,
        QueryParamTypes=dict,
        RequestContent=object,
        RequestFiles=object,
        AuthTypes=object,
        TimeoutTypes=object,
    )
    sys.modules['httpx'] = httpx

from fastapi.testclient import TestClient
import types as _types
import api.character_router as cr


def _mock_rate_limit(monkeypatch):
    monkeypatch.setattr(cr.r, 'incr', lambda *a, **k: 1)
    monkeypatch.setattr(cr.r, 'expire', lambda *a, **k: None)


def test_manifest_returns_manifest():
    with TestClient(cr.app) as client:
        resp = client.get('/manifest')
        assert resp.status_code == 200
        assert resp.json() == cr._load_manifest()


def test_chat(monkeypatch):
    _mock_rate_limit(monkeypatch)

    class Choice:
        message = _types.SimpleNamespace(content='hi')

    def fake_create(*args, **kwargs):
        return _types.SimpleNamespace(choices=[Choice()])

    monkeypatch.setattr(cr.client.chat.completions, 'create', fake_create)
    with TestClient(cr.app) as client:
        resp = client.post('/chat', json={'character': 'blueprint-nova', 'message': 'hey'})
        assert resp.status_code == 200
        assert resp.json() == {'reply': 'hi'}


def test_chat_stream(monkeypatch):
    _mock_rate_limit(monkeypatch)

    def fake_create(*args, **kwargs):
        assert kwargs.get('stream') is True

        class Chunk:
            def __init__(self, c: str):
                self.choices = [_types.SimpleNamespace(delta=_types.SimpleNamespace(content=c))]

        return [Chunk('A'), Chunk('B')]

    monkeypatch.setattr(cr.client.chat.completions, 'create', fake_create)
    with TestClient(cr.app) as client:
        resp = client.post('/chat/stream', json={'character': 'blueprint-nova', 'message': 'hey'})
        assert resp.status_code == 200
        assert resp.headers['content-type'].startswith('text/event-stream')
        assert resp.text == 'AB'


def test_chat_unknown_persona(monkeypatch):
    _mock_rate_limit(monkeypatch)

    def boom(*args, **kwargs):
        raise AssertionError("should not be called")

    monkeypatch.setattr(cr.client.chat.completions, 'create', boom)
    with TestClient(cr.app) as client:
        resp = client.post('/chat', json={'character': 'bogus', 'message': 'hi'})
        assert resp.status_code == 404
        assert resp.json() == {'detail': 'Persona not found'}


def test_chat_stream_unknown_persona(monkeypatch):
    _mock_rate_limit(monkeypatch)

    def boom(*args, **kwargs):
        raise AssertionError("should not be called")

    monkeypatch.setattr(cr.client.chat.completions, 'create', boom)
    with TestClient(cr.app) as client:
        resp = client.post('/chat/stream', json={'character': 'bogus', 'message': 'hi'})
        assert resp.status_code == 404
        assert resp.json() == {'detail': 'Persona not found'}
