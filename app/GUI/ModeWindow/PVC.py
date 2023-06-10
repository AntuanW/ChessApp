import chess

from app.Enums.modeEnum import GameMode
from app.Modes import PvComputer
from app.GUI.ModeWindow.StatsWindow import *
import requests

# Player VS Computer
class PVC:
    def __init__(self):
        p.init()
        self.window_width = 512
        self.window_height = 512
        self.window_title = "Player VS Computer Mode Window"
        self.mode = GameMode.PLAYER_VS_COMPUTER

        self.game_state = None
        self.last_difficulty = None
        self.date = None

        self.WHITE = (255, 255, 255)
        self.BLACK = (0, 0, 0)
        self.gray = (188, 188, 188)
        self.green = (0, 255, 0)

        self.font1 = p.font.SysFont("Arial", 20, bold=True)
        self.font2 = p.font.SysFont("Arial", 16, bold=True)

        self.font_size = 24
        self.font_color = self.BLACK

        self.screen = p.display.set_mode((self.window_width, self.window_height))
        p.display.set_caption(self.window_title)

        self.checkbox_value = False
        self.difficulty = 2

        self.running = True

    def handle_checkbox_click(self):
        self.checkbox_value = not self.checkbox_value

    def handle_slider_click(self, mouse_pos):
        slider_x = 50
        slider_width = 200
        mouse_x = mouse_pos[0]
        relative_x = mouse_x - slider_x
        normalized_value = relative_x / slider_width
        self.difficulty = int(normalized_value * 10) + 1

    def handle_start_button_click(self):

        if self.checkbox_value:
            color = chess.BLACK
        else:
            color = chess.WHITE

        print("Starting your game")
        print(f"Chosen color lvl: ${color}")
        print(f"Chosen difficulty lvl: ${self.difficulty}")

        self.running = False
        p.quit()

        # STARTING GAME

        PvComputer.game(color, self.difficulty)

    def handle_load_button_click(self):
        print("Loading your last saved game ...")
        if self.get_last_saved_game():
            p.quit()
            self.running = False
            PvComputer.game(self.get_color_from_str(self.game_state), self.last_difficulty, self.game_state)

    def handle_statistics_button_click(self):
        print("Go to statistics")
        StatsWindow(self.mode).run()

    def handle_go_back_click(self):
        p.quit()
        self.running = False

        from app.GUI.ModeWindow.ModeWindow import ModeWindow
        ModeWindow().run()
        print("Switching back window")

    def handle_event(self, event):

        if event.type == p.QUIT:
            self.running = False

        elif event.type == p.MOUSEBUTTONDOWN:
            mouse_pos = p.mouse.get_pos()
            checkbox_rect = p.Rect(50, 50, 20, 20)
            slider_rect = p.Rect(50, 100, 200, 20)
            start_button_rect = p.Rect(50, 150, 200, 50)
            load_button_rect = p.Rect(50, 230, 200, 50)
            statistics_button_rect = p.Rect(50, 420, 200, 50)
            go_back_rect = p.Rect(390, 20, 100, 25)

            if checkbox_rect.collidepoint(mouse_pos):
                self.handle_checkbox_click()
            elif slider_rect.collidepoint(mouse_pos):
                self.handle_slider_click(mouse_pos)
            elif start_button_rect.collidepoint(mouse_pos):
                self.handle_start_button_click()
            elif load_button_rect.collidepoint(mouse_pos):
                self.handle_load_button_click()
            elif statistics_button_rect.collidepoint(mouse_pos):
                self.handle_statistics_button_click()
            elif go_back_rect.collidepoint(mouse_pos):
                self.handle_go_back_click()

    def draw(self):
        self.screen.fill(self.WHITE)

        checkbox_rect = p.Rect(50, 50, 20, 20)
        p.draw.rect(self.screen, self.font_color, checkbox_rect, 2)

        if self.checkbox_value:
            p.draw.rect(self.screen, self.font_color, checkbox_rect)

        checkbox_label = p.font.Font(None, self.font_size).render("Play as White/Black", True, self.font_color)
        self.screen.blit(checkbox_label, (80, 50))

        slider_x = 50
        slider_y = 100
        slider_width = 200
        slider_height = 20
        slider_value = (self.difficulty - 1) / 9
        slider_rect = p.Rect(slider_x, slider_y, slider_width, slider_height)
        p.draw.rect(self.screen, self.font_color, slider_rect, 2)
        slider_fill_rect = p.Rect(slider_x, slider_y, int(slider_value * slider_width), slider_height)
        p.draw.rect(self.screen, self.font_color, slider_fill_rect)

        slider_label = p.font.Font(None, self.font_size).render("Difficulty: {}".format(self.difficulty),
                                                                True, self.font_color)
        self.screen.blit(slider_label, (slider_x + slider_width + 20, slider_y))

        start_button_rect = p.Rect(50, 150, 200, 50)
        p.draw.rect(self.screen, self.font_color, start_button_rect, 2)
        start_button_label = p.font.Font(None, self.font_size).render("Start Game", True, self.font_color)
        self.screen.blit(start_button_label, (105, 168))

        load_button_rect = p.Rect(50, 230, 200, 50)
        p.draw.rect(self.screen, self.font_color, load_button_rect, 2)
        load_button_label = p.font.Font(None, self.font_size).render("Load last saved & Play", True, self.font_color)
        self.screen.blit(load_button_label, (63, 248))

        statistics_button_rect = p.Rect(50, 420, 200, 50)
        p.draw.rect(self.screen, self.font_color, statistics_button_rect, 2)
        statistics_button_label = p.font.Font(None, self.font_size).render("Show Statistics",
                                                                            True, self.font_color)
        self.screen.blit(statistics_button_label, (90, 437))

        go_back_rect = p.Rect(390, 20, 100, 25)
        p.draw.rect(self.screen, self.gray, go_back_rect)
        register_text = self.font2.render("Go back", True, self.BLACK)
        register_text_rect = register_text.get_rect(center=(438, 33))
        self.screen.blit(register_text, register_text_rect)

        p.display.flip()

    def get_last_saved_game(self):

        data = {"username": get_username()}

        try:
            print("Getting last saved game ...")
            response = requests.post("http://localhost:8080/last_saved", json=data)
            if response.status_code == 200:
                response = response.json()
                print("Last saved game fetched succesfully from the server!")
                self.game_state = response['game_state']
                self.last_difficulty = response['difficulty']
                self.date = response['date']
                return True

            elif response.status_code == 406:
                print("You have no saved game")
                return False

            else:
                print("Failed to fetch the last saved game. Status code:", response.status_code)
                return False

        except requests.exceptions.RequestException as e:
            print("Error occurred during the request:", str(e))
            return False


    def get_color_from_str(self, game_state: str):

        if game_state.split(' ')[1] == 'w': return chess.WHITE
        else: return chess.BLACK

    def run(self):
        while self.running:
            for event in p.event.get():
                self.handle_event(event)

            if self.running:
                self.draw()

        p.quit()




