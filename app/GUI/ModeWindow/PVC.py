import chess
import pygame as p

from app.GUI.ModeWindow.ModeWindow import ModeWindow

from app.Modes import PvComputer

class PVC:

    def __init__(self):
        p.init()
        self.window_width = 512
        self.window_height = 512
        self.window_title = "Player VS Computer Mode Window"

        self.WHITE = (255, 255, 255)
        self.BLACK = (0, 0, 0)
        self.gray = (128, 128, 128)
        self.green = (0, 255, 0)

        self.font1 = p.font.SysFont("Arial", 20, bold=True)
        self.font2 = p.font.SysFont("Arial", 16, bold=True)

        self.font_size = 24
        self.font_color = self.BLACK

        self.screen = p.display.set_mode((self.window_width, self.window_height))
        p.display.set_caption(self.window_title)

        self.checkbox_value = False
        self.difficulty_level = 2

        self.running = True

    def run(self):

        while self.running:

            for event in p.event.get():

                if event.type == p.QUIT:
                    self.running = False

                elif event.type == p.MOUSEBUTTONDOWN:
                    mouse_pos = p.mouse.get_pos()

                    checkbox_rect = p.Rect(50, 50, 20, 20)

                    if checkbox_rect.collidepoint(mouse_pos):
                        self.checkbox_value = not self.checkbox_value

                    slider_rect = p.Rect(50, 100, 200, 20)

                    if slider_rect.collidepoint(mouse_pos):
                        mouse_x = mouse_pos[0]
                        relative_x = mouse_x - slider_rect.x
                        normalized_value = relative_x / slider_rect.width
                        self.difficulty_level = int(normalized_value * 10) + 1

                    start_button_rect = p.Rect(50, 150, 200, 50)

                    if start_button_rect.collidepoint(mouse_pos):


                        if self.checkbox_value:
                            color = chess.WHITE

                        else: color = chess.BLACK

                        print("Starting your game")

                        running = False
                        # p.quit()


                        # STARTING GAME

                        # PvComputer.game(color, self.difficulty_level)


                    statistics_button_rect = p.Rect(50, 420, 200, 50)

                    if statistics_button_rect.collidepoint(mouse_pos):
                        print("Go to statisctics")


                    go_back_rect = p.draw.rect(self.screen, self.gray, (390, 20, 100, 25))

                    if go_back_rect.collidepoint(mouse_pos):
                        # p.quit()
                        self.running = False

                        ModeWindow().run()
                        print("Switching back window")


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
            slider_value = (self.difficulty_level - 1) / 9
            slider_rect = p.Rect(slider_x, slider_y, slider_width, slider_height)
            p.draw.rect(self.screen, self.font_color, slider_rect, 2)
            slider_fill_rect = p.Rect(slider_x, slider_y, int(slider_value * slider_width), slider_height)
            p.draw.rect(self.screen, self.font_color, slider_fill_rect)

            slider_label = p.font.Font(None, self.font_size).render("Difficulty: {}".format(self.difficulty_level), True, self.font_color)
            self.screen.blit(slider_label, (slider_x + slider_width + 20, slider_y))

            start_button_rect = p.Rect(50, 150, 200, 50)
            p.draw.rect(self.screen, self.font_color, start_button_rect, 2)
            start_button_label = p.font.Font(None, self.font_size).render("Start Game", True, self.font_color)
            self.screen.blit(start_button_label, (105, 168))

            statistics_button_rect = p.Rect(50, 420, 200, 50)
            p.draw.rect(self.screen, self.font_color, statistics_button_rect, 2)
            statistics_button_label = p.font.Font(None, self.font_size).render("Show Statistics", True, self.font_color)
            self.screen.blit(statistics_button_label, (90, 437))

            p.draw.rect(self.screen, self.gray, (390, 20, 100, 25))
            register_text = self.font2.render("Go back", True, self.BLACK)
            register_text_rect = register_text.get_rect(center=(438, 33))
            self.screen.blit(register_text, register_text_rect)

            p.display.flip()

        p.quit()



