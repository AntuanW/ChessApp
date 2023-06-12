import chess
import pygame as p
import requests

from app.Enums.modeEnum import GameMode
from app.config import get_username

WIDTH = 800
HEIGHT = 600
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)


class EndgameWindow:
    def __init__(self, our_color: chess.Color, game_state: str,
                 outcome: chess.Outcome, difficulty: int, game_mode):
        p.init()
        self.window_width = 512
        self.window_height = 512
        self.window_title = "Game over"
        self.game_state = game_state
        self.font = p.font.Font(None, 52)
        self.button_font = p.font.Font(None, 30)
        self.running = True
        self.our_color = our_color
        self.outcome = outcome
        self.score = self.set_score()
        self.winner_color = self.get_winner_color()
        self.difficulty = difficulty

        if game_mode == GameMode.PLAYER_VS_COMPUTER:
            print("saving to database mode: PVC")
            self.add_score()

        else:
            print("not saving to database mode: PVP Local")

        self.screen = p.display.set_mode((self.window_width, self.window_height))
        p.display.set_caption(self.window_title)

    def get_winner_color(self):
        if self.score == -1:
            return "You lose"
        elif self.score == 1:
            return "You win"
        else:
            return "Draw"

    def add_score(self):
        data = {
            "username": get_username(),
            "res": self.score,
            "game_state": self.game_state,
            "difficulty": self.difficulty
        }
        try:
            print("Adding score to the database...")
            response = requests.put("http://localhost:8080/score", json=data)
            if response.status_code == 200:
                print("Score added successfully to the database")
            else:
                print("Failed to add data to the database. Status code:", response.status_code)
        except requests.exceptions.RequestException as e:
            print("Error occurred during the request:", str(e))

    def draw(self):
        self.screen.fill(WHITE)
        p.display.set_caption("GAME OVER!")

        game_over_text = self.font.render("Game Over due to:", True, BLACK)
        game_over_text_rect = game_over_text.get_rect(center=(WIDTH // 3.1, HEIGHT // 3 - 100))

        result_text = self.font.render(self.outcome.termination.name, True, BLACK)
        result_text_rect = result_text.get_rect(center=(WIDTH // 3.1, HEIGHT // 3))

        if self.our_color is None:
            if self.outcome.winner:
                out = "White Won!"
            elif self.outcome.winner is not None:
                out = "Black Won!"
            else:
                out = ""
            winner_text = self.font.render(out, True, BLACK)
        else:
            winner_text = self.font.render(self.winner_color, True, BLACK)
        winner_text_rect = winner_text.get_rect(center=(WIDTH // 3.1, HEIGHT // 3 + 100))

        self.screen.blit(game_over_text, game_over_text_rect)
        self.screen.blit(result_text, result_text_rect)
        self.screen.blit(winner_text, winner_text_rect)

        button_text = self.button_font.render("Go Back", True, BLACK)
        button_rect = button_text.get_rect(center=(self.window_width // 2, self.window_height - 50))
        button_padding = 15
        self.button_area = p.Rect(button_rect.left - button_padding, button_rect.top - button_padding,
                                  button_rect.width + 2 * button_padding, button_rect.height + 2 * button_padding)

        p.draw.rect(self.screen, p.Color(188, 188, 188), self.button_area)
        self.screen.blit(button_text, button_rect)

        p.display.flip()

    def run(self):
        self.running = True
        self.draw()
        while self.running:
            for event in p.event.get():
                if event.type == p.QUIT:
                    self.running = False
                    p.quit()
                elif event.type == p.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        if self.button_area.collidepoint(event.pos):
                            self.running = False
                            p.quit()
                            from app.GUI.ModeWindow.ModeWindow import ModeWindow
                            ModeWindow().run()

                    if self.running:
                        self.draw()
        return False

    def set_score(self):
        if self.outcome.winner is None:
            return 0  # draw
        elif self.outcome.winner == self.our_color:
            return 1  # win
        else:
            return -1  # lose
