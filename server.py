from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from urllib.request import Request, urlopen
import sys
import webbrowser


PORT = 8765
TV_URL = "https://www.tdtchannels.com/lists/tv.json"


class TdtHandler(SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/api/tv":
            self.send_tdt_list()
            return
        super().do_GET()

    def send_tdt_list(self):
        try:
            request = Request(TV_URL, headers={"User-Agent": "TV Nacional local app"})
            with urlopen(request, timeout=20) as response:
                body = response.read()
        except Exception as error:
            body = ('{"error": "%s"}' % str(error).replace('"', "'")).encode("utf-8")
            self.send_response(502)
        else:
            self.send_response(200)

        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(body)


if __name__ == "__main__":
    address = ("127.0.0.1", PORT)
    print(f"TV Nacional abierto en http://{address[0]}:{address[1]}/")
    if "--no-open" not in sys.argv:
        webbrowser.open(f"http://{address[0]}:{address[1]}/")
    ThreadingHTTPServer(address, TdtHandler).serve_forever()
