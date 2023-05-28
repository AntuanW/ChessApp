import pygame as p
import requests

from app.config import get_username


class StatsWindow:

    def __init__(self, mode):
        p.init()
        self.mode = mode
        self.WIDTH, self.HEIGHT = 512, 512
        self.WHITE = p.Color("White")
        self.BLACK = p.Color("Black")
        self.HOVER_WHITE = p.Color(225, 225, 225)
        self.HOVER_BLACK = p.Color(65, 65, 65)
        self.running = True
        self.wins = 0
        self.loses = 0

        self.screen = p.display.set_mode((self.WIDTH, self.HEIGHT))
        self.clock = p.time.Clock()
        p.display.set_caption("Statistics Window")
        self.font1 = p.font.SysFont("Arial", 30, bold=True)
        self.font2 = p.font.SysFont("Arial", 20, bold=True)
        self.font3 = p.font.SysFont("Arial", 16, bold=True)
        self.font4 = p.font.SysFont("Arial", 10)
        self.button_width = 300
        self.button_height = 70
        self.button_padding = 20
        self.button_y = self.HEIGHT // 4

        self.label1_x = (self.WIDTH - self.font1.render("Statistics", True, self.BLACK).get_width()) // 2
        self.label1_y = self.button_y - self.font1.get_height()

        self.label2_x = (self.WIDTH - self.font2.render(self.mode.value, True, self.BLACK).get_width()) // 2
        self.label2_y = self.button_y - self.font2.get_height() + 40

        self.label3_x = (self.WIDTH - self.font1.render(f"wins: {self.wins}", True, self.BLACK).get_width()) // 2
        self.label3_y = self.button_y - self.font1.get_height() + 120

        self.label4_x = (self.WIDTH - self.font1.render(f"loses: {self.loses}", True, self.BLACK).get_width()) // 2
        self.label4_y = self.button_y - self.font1.get_height() + 165

    def getStatistics(self):

        data = {"username": get_username(),
                "mode": self.mode.value}

        try:

            print("Getting statistics ...")
            response = requests.post("http://localhost:8080/stats", json=data)

            if response.status_code == 200:
                response = response.json()
                print(response['message'])
                self.wins = response['wins']
                self.loses = response['loses']
                print(self.wins)
                print(self.loses)

            else:
                print("Failed to fetch statistics. Status code:", response.status_code)

        except requests.exceptions.RequestException as e:
            print("Error occurred during the request:", str(e))

    def draw(self):

        self.screen.fill(self.WHITE)

        label1 = self.font1.render("Statistics", True, self.BLACK)
        self.screen.blit(label1, (self.label1_x, self.label1_y))

        label2 = self.font2.render(self.mode.value, True, self.BLACK)
        self.screen.blit(label2, (self.label2_x, self.label2_y))

        label3 = self.font1.render(f"wins: {self.wins}", True, self.BLACK)
        self.screen.blit(label3, (self.label3_x, self.label3_y))

        label4 = self.font1.render(f"loses: {self.loses}", True, self.BLACK)
        self.screen.blit(label4, (self.label4_x, self.label4_y))

        p.display.flip()

    def run(self):

        self.getStatistics()

        while self.running:

            for event in p.event.get():

                if event.type == p.QUIT:
                    self.running = False
                    p.quit()

                # elif event.type == p.MOUSEBUTTONUP:
                #     self.running = False

            if self.running:
                self.draw()

        p.quit()


# StatsWindow(GameMode.PLAYER_VS_COMPUTER).run()
# getStatistics()