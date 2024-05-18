import time

from wifi import connect_wlan
from ws_connection import ClientClosedError
from ws_server import WebSocketClient, WebSocketServer


class TestClient(WebSocketClient):
    def __init__(self, conn):
        super().__init__(conn)

    def process(self):
        try:
            msg = self.connection.read()
            if not msg:
                return
            msg = msg.decode("utf-8")
            items = msg.split(" ")
            cmd = items[0]
            if cmd == "Hello":
                self.connection.write(cmd + " World")
                print("Hello World")
            else:
                self.connection.write(cmd + " Response")
                print(cmd + " Response")
        except ClientClosedError:
            self.connection.close()


class TestServer(WebSocketServer):
    def __init__(self):
        super().__init__("index.html", 4)

    def _make_client(self, conn):
        return TestClient(conn)


print("Connecting to wlan...")
connect_wlan()
server = TestServer()
server.start()

times_processed = 0
start = time.ticks_ms()
try:
    while True:
        server.process_all()
        times_processed += 1
        if times_processed % 200 == 0:
            current = time.ticks_ms()
            print(f"Took {current - start}ms to do another 200 requests ({times_processed} total)")
            start = current

except KeyboardInterrupt:
    pass
server.stop()
