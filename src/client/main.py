import socket
import threading

from kivy.app import App
from kivy.config import Config

from gui import GameScreen


class Socket:
    def __init__(self, host='localhost', port=20001):
        self.sock = socket.socket()
        self.sock.connect((host, port))
    
    def get_msg(self):
        return self.sock.recv(1024)
    
    def send_msg(self, msg):
        self.sock.send(msg)
    
    def close(self):
        self.sock.close()


class SocketThread(threading.Thread):
    def __init__(self, *args, **kwargs):
        super(SocketThread, self).__init__(*args, **kwargs)
        self.stop_event = threading.Event()
    
    def stop(self):
        self.stop_event.set()
    
    def stopped(self):
        self.stop_event.is_set()
    
    def run(self):
        app = App.get_running_app()

        while True:
            if self.stopped(): break
            msg = app.socket.get_msg()
            print(msg)

            msg = msg.split(sep=b':')
            pos_str = msg[1].split(sep=b'#')
            x,y = map(lambda a: int(a), pos_str)

            app.root.board[x][y].press()
            print(x, y)


class GameApp(App):
    def build(self):
        self.symbols = ['X', 'O']
        self.current_turn = 0
        self.player_turn = 0
        self.socket = Socket()

        msg = self.socket.get_msg().split(sep=b':')
        
        if msg[1] == b'O': self.player_turn = 1

        self.sock_thr = SocketThread()
        self.sock_thr.start()

        return GameScreen()

    def send_msg(self, msg):
        msg += ':{}'.format(self.symbols[self.player_turn])
        self.socket.send_msg(msg.encode('utf-8'))

    def thr(self):
        while True:
            msg = self.socket.get_msg()
            print(msg)

            msg = msg.split(sep=b':')
            pos_str = msg[1].split(sep=b'#')
            x,y = map(lambda a: int(a), pos_str)

            self.root.board[x][y].press()
            print(x, y)

    def can_play(self):
        return self.player_turn == self.current_turn

    def get_symbol(self):
        symbol = self.symbols[self.current_turn]

        self.current_turn += 1
        self.current_turn %= 2

        return symbol


Config.set('graphics', 'width', '450')
Config.set('graphics', 'height', '200')

GameApp().run()