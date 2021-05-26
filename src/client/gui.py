from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.screenmanager import Screen


class GameButton(Button):
    def on_release(self):
        app = App.get_running_app()

        if app.can_play():
            x,y = self.grid_pos
            msg = '{}#{}'.format(x, y)
            app.send_move(msg)
            self.press()
    
    def press(self):
        if not self.disabled:
            app = App.get_running_app()

            self.text = app.get_symbol()
            self.font_size = self.width
            self.disabled = True

            app.game.update_player_labels()

    def set_grid_pos(self, pos):
        self.grid_pos = pos


class GameGrid(GridLayout):
    def __init__(self, board, **kwargs):
        super(GameGrid, self).__init__(**kwargs)
        
        self.rows = len(board)
        self.cols = self.rows

        for i in range(self.cols):
            for j in range(self.rows):
                board[i][j].set_grid_pos((i,j))

                button_box = AnchorLayout()
                button_box.add_widget(board[i][j])
                self.add_widget(button_box)


class GameScreen(BoxLayout):
    playerLabels = [None, None]

    def __init__(self, **kwargs):
        super(GameScreen, self).__init__()

        self.padding = [15]
        self.spacing = 10

        self._draw_grid()
        self._draw_right_widgets()

        self.update_player_labels()

    def update_player_labels(self):
        turn = App.get_running_app().current_turn

        self.playerLabels[turn].bold = True
        self.playerLabels[turn].color = (1, 1, 1, 1)

        self.playerLabels[turn - 1].bold = False
        self.playerLabels[turn - 1].color = (1, 1, 1, .3)

    def _draw_grid(self):
        self.board = [[GameButton() for j in range(3)] for i in range(3)]
        grid = GameGrid(self.board)

        self.add_widget(grid)

    def _draw_right_widgets(self):
        box = BoxLayout(orientation='vertical')

        title = Label(
            text = 'TicTacToe',
            bold = True,
            font_size = 30
        )

        player_box = self._create_player_box()
        exit_button = self._create_exit_button()
        
        box.add_widget(title)
        box.add_widget(player_box)
        box.add_widget(exit_button)

        self.add_widget(box)

    def _create_player_box(self):
        player_box = BoxLayout(padding=[10], spacing=10)

        player_turn = App.get_running_app().player_turn
        symbols = App.get_running_app().symbols

        your_label = Label(
            text = f"You: '{symbols[player_turn]}'",
            font_size = 20
        )
        your_foe_label = Label(
            text = f"Foe: '{symbols[player_turn - 1]}'",
            font_size = 20
        )

        self.playerLabels[player_turn] = your_label
        self.playerLabels[player_turn - 1] = your_foe_label

        player_box.add_widget(self.playerLabels[player_turn])
        player_box.add_widget(self.playerLabels[player_turn - 1])

        return player_box

    def _create_exit_button(self):
        exit_box = AnchorLayout(anchor_x='center', anchor_y='center')
        
        exit_button = Button(
            text = 'Exit',
            background_color = [1,0.4,0.4,1],
            size_hint = (0.7,0.5),
            on_release = App.get_running_app().close
        )
        
        exit_box.add_widget(exit_button)

        return exit_box


class StartScreen(Screen):
    pass

class DisconnectScreen(Screen):
    pass

class EndGamePopup(Popup):
    def on_dismiss(self):
        App.get_running_app().close()