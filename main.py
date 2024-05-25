import time

from wifi import connect_wlan
from ws_connection import ClientClosedError
from ws_server import WebSocketClient, WebSocketServer
from machine import Pin

onboard_led = Pin("LED", Pin.OUT)


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
    
    def send_heartbeat(self):
        self.connection.write("heartbeat")


class TestServer(WebSocketServer):
    HEARTBEAT_MS = 1000

    def __init__(self):
        super().__init__("index.html", 4)
        self._previous_heartbeat = time.ticks_ms()
        self.i = 1

    def _make_client(self, conn):
        return TestClient(conn)
    
    def process_all(self):
        for client in self._clients:
            client.process()

    def hearbeat_all(self):
        current = time.ticks_ms()
        if current - self._previous_heartbeat < TestServer.HEARTBEAT_MS:
            return
        
        if self.i % 8 == 0:
            for client in self._clients:
                client.connection.write("trigger " + str(((self.i // 8) % 4) + 1))
        self.i += 1
        
        onboard_led.toggle()

        self._previous_heartbeat = current
        for client in self._clients:
            client.send_heartbeat()


print("Connecting to wlan...")
connect_wlan()
server = TestServer()
server.start()

try:
    while True:
        server.process_all()
        server.hearbeat_all()

except KeyboardInterrupt:
    pass
server.stop()
