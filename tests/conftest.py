import http.server
import os
import socketserver
import threading

import pytest

_REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
_PUBLIC_DIR = os.path.join(_REPO_ROOT, "public")


def _handler_factory(directory):
    class _Handler(http.server.SimpleHTTPRequestHandler):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, directory=directory, **kwargs)

    return _Handler


def _find_free_port() -> int:
    with socketserver.TCPServer(("127.0.0.1", 0), None) as s:
        return s.server_address[1]


@pytest.fixture(scope="session")
def base_url():
    port = _find_free_port()
    handler = _handler_factory(_PUBLIC_DIR)

    class _ThreadingTCPServer(socketserver.ThreadingTCPServer):
        allow_reuse_address = True

    httpd = _ThreadingTCPServer(("127.0.0.1", port), handler)

    thread = threading.Thread(target=httpd.serve_forever, daemon=True)
    thread.start()

    yield f"http://127.0.0.1:{port}"

    httpd.shutdown()
    httpd.server_close()
