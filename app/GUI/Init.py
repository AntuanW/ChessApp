import pygame as p

WIDTH, HEIGHT = 512, 512

WHITE = p.Color("White")
BLACK = p.Color("Black")
HOVER_WHITE = p.Color(225, 225, 225)
HOVER_BLACK = p.Color(65, 65, 65)

class GameWindow():
    def __init__(self):
        p.init()
        self.screen = p.display.set_mode((WIDTH, HEIGHT))
        self.clock = p.time.Clock()
        p.display.set_caption("CHESS")
        self.font1 = p.font.SysFont("Arial", 24, bold=True)
        self.font2 = p.font.SysFont("Arial", 16, bold=True)
        self.button_width = 300
        self.button_height = 70
        self.button_padding = 20
        self.button_x = (WIDTH - self.button_width) // 2
        self.button_y = HEIGHT // 4
        self.label_x = (WIDTH - self.font1.render("CHESS.COM SUCKS, WE ARE BETTER", True, BLACK).get_width()) // 2
        self.label_y = self.button_y - self.font1.get_height() - 40

        self.btn_img1 = p.image.load("../../resources/bN.png").convert_alpha()
        self.btn_img2 = p.image.load("../../resources/wQ.png").convert_alpha()
        self.btn_img3 = p.image.load("../../resources/bR.png").convert_alpha()
        self.btn_img4 = p.image.load("../../resources/wB.png").convert_alpha()

        self.btn_img1 = p.transform.scale(self.btn_img1, (self.button_height * 0.8, self.button_height * 0.8))
        self.btn_img2 = p.transform.scale(self.btn_img2, (self.button_height * 0.8, self.button_height * 0.8))
        self.btn_img3 = p.transform.scale(self.btn_img3, (self.button_height * 0.8, self.button_height * 0.8))
        self.btn_img4 = p.transform.scale(self.btn_img4, (self.button_height * 0.8, self.button_height * 0.8))

    def draw_buttons(self):
        button_texts = ["TRYB GRY 1", "TRYB GRY 2", "TRYB GRY 3", "CHESS GM's"]
        button_images = [self.btn_img1, self.btn_img2, self.btn_img3, self.btn_img4]

        for i in range(4):
            button_rect = p.Rect(self.button_x, self.button_y + i * (self.button_height + self.button_padding),
                                 self.button_width, self.button_height)
            if i % 2:
                button_color = BLACK
                text_color = WHITE

            else:
                button_color = WHITE
                text_color = BLACK

            if button_rect.collidepoint(p.mouse.get_pos()):
                if i % 2: button_color = HOVER_BLACK
                else: button_color = HOVER_WHITE

            p.draw.rect(self.screen, button_color, button_rect, 0)
            p.draw.rect(self.screen, BLACK, button_rect, 2)

            button_image_x = self.button_x + 10
            button_image_y = self.button_y + i * (self.button_height + self.button_padding) + (
                    self.button_height - self.btn_img1.get_height()) // 2
            self.screen.blit(button_images[i], (button_image_x, button_image_y))

            label = self.font2.render(button_texts[i], True, text_color)
            label_x = self.button_x + self.button_width // 2 - label.get_width() // 2
            label_y = self.button_y + i * (self.button_height + self.button_padding) + (
                    self.button_height - label.get_height()) // 2
            self.screen.blit(label, (label_x, label_y))

    def run(self):
        running = True
        while running:

            for event in p.event.get():
                if event.type == p.QUIT:
                    running = False

            self.screen.fill(WHITE)
            self.draw_buttons()

            label = self.font1.render("CHESS.COM SUCKS, WE ARE BETTER", True, BLACK)
            self.screen.blit(label, (self.label_x, self.label_y))

            p.display.flip()
            self.clock.tick(60)

        p.quit()


x = GameWindow()
x.run()
