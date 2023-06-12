import pygame as p
import requests


class RankingWindow:
    def __init__(self):
        p.init()
        self.top_10 = []
        self.fetchTopPlayers()
        self.WIDTH, self.HEIGHT = 512, 512
        self.WHITE = p.Color("White")
        self.BLACK = p.Color("Black")
        self.gray = p.Color(188, 188, 188)
        self.HOVER_WHITE = p.Color(225, 225, 225)
        self.HOVER_BLACK = p.Color(65, 65, 65)
        self.running = True

        self.screen = p.display.set_mode((self.WIDTH, self.HEIGHT))
        p.display.set_caption("Ranking Window")
        self.font1 = p.font.SysFont("Arial", 30, bold=True)
        self.font2 = p.font.SysFont("Arial", 20, bold=True)
        self.font3 = p.font.SysFont("Arial", 16, bold=True)
        self.font4 = p.font.SysFont("Arial", 10)
        self.button_width = 300
        self.button_height = 70
        self.button_padding = 20
        self.button_x = (self.WIDTH - self.button_width) // 2
        self.button_y = self.HEIGHT // 4

    def fetchTopPlayers(self):

        # FETCHING ARRAY OF TOP 10 PLAYERS

        try:

            print("Getting top 10 players ...")
            response = requests.get("http://localhost:8080/top_players")

            if response.status_code == 200:
                response = response.json()
                self.top_10 = response['top_10']
                # print(self.top_10)

            else:
                print("Failed to fetch top players. Status code:", response.status_code)

        except requests.exceptions.RequestException as e:
            print("Error occurred during the request:", str(e))

    def handle_button_click(self, event):
        if event.type == p.QUIT:
            self.running = False
        elif event.type == p.MOUSEBUTTONDOWN:
            mouse_pos = p.mouse.get_pos()
            go_back_rect = p.Rect(390, 20, 100, 25)
            if go_back_rect.collidepoint(mouse_pos):
                self.handle_go_back_click()

    def handle_go_back_click(self):
        p.quit()
        self.running = False
        print("Switching back window")
        from app.GUI.ModeWindow.ModeWindow import ModeWindow
        ModeWindow().run()

    def draw_top_players_label(self):
        label_text = "Top Players"
        label_render = self.font1.render(label_text, True, self.BLACK)
        label_rect = label_render.get_rect(center=(self.WIDTH // 2, self.HEIGHT // 7))
        self.screen.blit(label_render, label_rect)

    def draw_players(self):
        player_start_y = self.HEIGHT // 20 + self.button_height + self.button_padding * 2 + 20
        player_spacing = 30

        for i, player in enumerate(self.top_10):
            player_text = f"{i + 1}. {player['playername']}  {round(player['ranking'], 2)}"
            player_render = self.font3.render(player_text, True, self.BLACK)
            player_rect = player_render.get_rect(
                topleft=(self.WIDTH // 2 - 85, player_start_y + i * player_spacing)
            )
            self.screen.blit(player_render, player_rect)

            if i < 3:
                medal_image = p.image.load(f"../resources/Medals/medal_{i + 1}.png")
                medal_image = p.transform.scale(medal_image, (25, 25))
                medal_rect = medal_image.get_rect(
                    topleft=(self.WIDTH // 2 - 120, player_start_y + i * player_spacing - 3)
                )
                self.screen.blit(medal_image, medal_rect)

    def draw_player_labels(self):
        player_label_text = "Player Name & Ranking"
        player_label_render = self.font2.render(player_label_text, True, self.BLACK)
        player_label_rect = player_label_render.get_rect(
            topleft=(self.WIDTH // 2 - 120, self.HEIGHT // 20 + self.button_height + self.button_padding)
        )
        self.screen.blit(player_label_render, player_label_rect)

    def draw(self):
        self.screen.fill(self.WHITE)
        self.draw_top_players_label()
        self.draw_players()
        # self.draw_medals()
        self.draw_player_labels()

        go_back_rect = p.Rect(390, 20, 100, 25)
        p.draw.rect(self.screen, self.gray, go_back_rect)
        register_text = self.font3.render("Go back", True, self.BLACK)
        register_text_rect = register_text.get_rect(center=(438, 33))
        self.screen.blit(register_text, register_text_rect)

        p.display.flip()

    def run(self):
        while self.running:
            for event in p.event.get():
                if event.type == p.QUIT:
                    self.running = False
                    p.quit()
                elif event.type == p.MOUSEBUTTONDOWN:
                    self.handle_button_click(event)

            if self.running:
                self.draw()

        p.quit()
