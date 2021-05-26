import socket
import threading

from kivy.app import App
from kivy.config import Config
from kivy.uix.label import Label

from kivy.uix.screenmanager import (ScreenManager, Screen)

from gui import (GameScreen, StartScreen, DisconnectScreen, EndGamePopup)


class Socket:
    def __init__(self, host='Orpheus', port=6544):
        self.sock = socket.socket()
        self.sock.connect((host, port))
    
    def get_msg(self):
        return self.sock.recv(1024)
    
    def send_msg(self, msg: bytes):
        self.sock.send(msg)
    
    def close(self):
        self.sock.close()


class SocketThread(threading.Thread):   
    def run(self):
        app = App.get_running_app()

        while True:
            msg = app.socket.get_msg().decode()

            if msg == 'DESCONECTAR':
                break

            msg = msg.split(sep=':')
            
            pos_str = msg[1].split(sep='#')
            x,y = map(lambda a: int(a), pos_str)

            app.game.board[x][y].press()

            if msg[0] == 'VENCEU':
                popup = EndGamePopup(title="You've won!")
                popup.open()
            
            elif msg[0] == 'PERDEU':
                popup = EndGamePopup(title="You've lost!")
                popup.open()
            
            elif msg[0] == 'EMPATE':
                popup = EndGamePopup(title="It's a tie!")
                popup.open()


class GameApp(App):
    def build(self):
        self.symbols = ['X', 'O']
        self.current_turn = 0
        self.player_turn = 0
        self.socket = Socket()

        sm = ScreenManager()
        
        sm.add_widget(StartScreen())
        sm.add_widget(DisconnectScreen())

        sm.current = 'start'

        thr = threading.Thread(target=self.start_game)
        thr.start()

        return sm

    def start_game(self):
        msg = self.socket.get_msg().split(sep=b':')

        if msg[1] == b'O': self.player_turn = 1

        self.game = GameScreen()
        game = Screen(name='game')
        game.add_widget(self.game)

        self.root.add_widget(game)
        self.root.current = 'game'

        self.sock_thr = SocketThread()
        self.sock_thr.start()

    def send_move(self, msg):
        msg += ':{}'.format(self.symbols[self.player_turn])
        self.socket.send_msg(msg.encode('utf-8'))

    def can_play(self):
        return self.player_turn == self.current_turn

    def get_symbol(self):
        symbol = self.symbols[self.current_turn]

        self.current_turn += 1
        self.current_turn %= 2

        return symbol

    def close(self, instance=None):
        self.root.current = 'disconnect'
        self.socket.send_msg(b'DESCONECTAR')
        self.stop()


Config.set('graphics', 'width', '450')
Config.set('graphics', 'height', '200')

GameApp().run()