import pygame as p
from app.GUI.ModeWindow.PVC import PVC

class ModeWindow:
    def __init__(self):
        p.init()
        self.WIDTH, self.HEIGHT = 512, 512
        self.WHITE = p.Color("White")
        self.BLACK = p.Color("Black")
        self.HOVER_WHITE = p.Color(225, 225, 225)
        self.HOVER_BLACK = p.Color(65, 65, 65)

        self.screen = p.display.set_mode((self.WIDTH, self.HEIGHT))
        self.clock = p.time.Clock()
        p.display.set_caption("CHESS ME!")
        self.font1 = p.font.SysFont("Arial", 30, bold=True)
        self.font2 = p.font.SysFont("Arial", 20, bold=True)
        self.font3 = p.font.SysFont("Arial", 16, bold=True)
        self.font4 = p.font.SysFont("Arial", 10)
        self.button_rects = []
        self.button_width = 300
        self.button_height = 70
        self.button_padding = 20
        self.button_x = (self.WIDTH - self.button_width) // 2
        self.button_y = self.HEIGHT // 4

        self.label1_x = (self.WIDTH - self.font1.render("CHESS.ME.COM", True, self.BLACK).get_width()) // 2
        self.label1_y = self.button_y - self.font1.get_height() - 60

        self.label2_x = (self.WIDTH - self.font2.render("CHESS.COM SUCKS, WE ARE BETTER", True, self.BLACK).get_width()) // 2
        self.label2_y = self.button_y - self.font2.get_height() - 20

        self.btn_images = [
            p.transform.scale(p.image.load("../resources/ChessImg/bN.png").convert_alpha(),
                              (int(self.button_height * 0.8), int(self.button_height * 0.8))),
            p.transform.scale(p.image.load("../resources/ChessImg/wQ.png").convert_alpha(),
                              (int(self.button_height * 0.8), int(self.button_height * 0.8))),
            p.transform.scale(p.image.load("../resources/ChessImg/bR.png").convert_alpha(),
                              (int(self.button_height * 0.8), int(self.button_height * 0.8))),
            p.transform.scale(p.image.load("../resources/ChessImg/wB.png").convert_alpha(),
                              (int(self.button_height * 0.8), int(self.button_height * 0.8)))
        ]

    def draw_buttons(self):
        button_texts = ["Player VS Computer", "Player VS Player (Local)", "Player VS Player (Online)", "CHESS GM's"]

        for i in range(4):
            button_rect = p.Rect(self.button_x, self.button_y + i * (self.button_height + self.button_padding),
                                 self.button_width, self.button_height)

            if i % 2:
                button_color = self.BLACK
                text_color = self.WHITE
            else:
                button_color = self.WHITE
                text_color = self.BLACK

            if button_rect.collidepoint(p.mouse.get_pos()):
                if i % 2:
                    button_color = self.HOVER_BLACK
                else:
                    button_color = self.HOVER_WHITE

            p.draw.rect(self.screen, button_color, button_rect, 0)
            p.draw.rect(self.screen, self.BLACK, button_rect, 2)

            button_image_x = self.button_x + 10
            button_image_y = self.button_y + i * (self.button_height + self.button_padding) + (
                    self.button_height - self.btn_images[i].get_height()) // 2
            self.screen.blit(self.btn_images[i], (button_image_x, button_image_y))

            label = self.font3.render(button_texts[i], True, text_color)
            label_x = self.button_x + self.button_width // 2 - label.get_width() // 2
            label_y = self.button_y + i * (self.button_height + self.button_padding) + (
                    self.button_height - label.get_height()) // 2
            self.screen.blit(label, (label_x, label_y))

    def handle_button_click(self, button_index):
        if button_index == 0:
            print("Button 1 clicked")
            PVC().run()
        elif button_index == 1:
            print("Button 2 clicked")
        elif button_index == 2:
            print("Button 3 clicked")
        elif button_index == 3:
            print("Button 4 clicked")

    def run(self):
        running = True
        while running:
            for event in p.event.get():
                if event.type == p.QUIT:
                    running = False
                    p.quit()
                elif event.type == p.MOUSEBUTTONUP:
                    mouse_pos = p.mouse.get_pos()
                    for i in range(4):
                        button_rect = p.Rect(self.button_x, self.button_y + i * (self.button_height + self.button_padding),
                                             self.button_width, self.button_height)

                        if button_rect.collidepoint(mouse_pos):
                            self.handle_button_click(i)
                            running = False

            self.screen.fill(self.WHITE)
            self.draw_buttons()

            label1 = self.font1.render("CHESS.ME.COM", True, self.BLACK)
            self.screen.blit(label1, (self.label1_x, self.label1_y))

            label2 = self.font2.render("CHESS.COM SUCKS, WE ARE BETTER", True, self.BLACK)
            self.screen.blit(label2, (self.label2_x, self.label2_y))

            p.display.flip()
            self.clock.tick(60)

        p.quit()

# ModeWindow().run()
