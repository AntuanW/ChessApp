import pygame as p
import requests

from app.GUI.ModeWindow.ModeWindow import ModeWindow
from app.config import set_username, MAX_FRAMERATE


class RegistrationWindow:
    def __init__(self):
        p.init()
        self.clock = p.time.Clock()
        self.width, self.height = 500, 500
        self.screen = p.display.set_mode((self.width, self.height))
        self.message_screen = None
        p.display.set_caption("Registration Window")

        self.white = (255, 255, 255)
        self.black = (0, 0, 0)
        self.gray = (188, 188, 188)
        self.green = (0, 255, 0)

        self.font1 = p.font.SysFont("Arial", 20, bold=True)
        self.font2 = p.font.SysFont("Arial", 16, bold=True)

        self.username = ""
        self.password = ""
        self.repeat_password = ""
        self.input_box_width = 200
        self.input_box_height = 40
        self.input_box_x = self.width // 2 - self.input_box_width // 2
        self.input_box_y = self.height // 2 - self.input_box_height

        self.register_button_width = 200
        self.register_button_height = 40
        self.register_button_x = self.width // 2 - self.register_button_width // 2
        self.register_button_y = self.height // 2 + self.input_box_height + 20

        self.running = True
        self.input_active = ""

        self.login_button_width = 270
        self.login_button_height = 30
        self.login_button_x = self.width - self.register_button_width - 100
        self.login_button_y = 40

    def handle_input(self, event):

        if event.key == p.K_BACKSPACE:
            if self.username and self.input_active == "username":
                self.username = self.username[:-1]
            elif self.password and self.input_active == "password":
                self.password = self.password[:-1]
            elif self.repeat_password and self.input_active == "repeat_password":
                self.repeat_password = self.repeat_password[:-1]
        else:
            if self.input_active == "username" and len(self.username) < 10:
                self.username += event.unicode
            elif self.input_active == "password" and len(self.password) < 10:
                self.password += event.unicode
            elif self.input_active == "repeat_password" and len(self.repeat_password) < 10:
                self.repeat_password += event.unicode

    def handle_mouse_click(self):

        mouse_pos = p.mouse.get_pos()

        input_box_username_rect = p.Rect(self.input_box_x + 15, self.input_box_y - 100, self.input_box_width,
                                         self.input_box_height)
        input_box_password_rect = p.Rect(self.input_box_x + 15, self.input_box_y - 20, self.input_box_width,
                                         self.input_box_height)
        input_box_repeat_password_rect = p.Rect(self.input_box_x + 15, self.input_box_y + 60, self.input_box_width,
                                                self.input_box_height)
        register_button_rect = p.Rect(self.register_button_x + 15, self.register_button_y + 40,
                                      self.register_button_width,
                                      self.register_button_height)

        if input_box_username_rect.collidepoint(mouse_pos):
            self.input_active = "username"
        elif input_box_password_rect.collidepoint(mouse_pos):
            self.input_active = "password"
        elif input_box_repeat_password_rect.collidepoint(mouse_pos):
            self.input_active = "repeat_password"
        elif register_button_rect.collidepoint(mouse_pos):
            self.register_user()
        else:
            self.input_active = ""

        login_button_rect = p.Rect(self.login_button_x, self.login_button_y, self.login_button_width,
                                   self.login_button_height)
        if login_button_rect.collidepoint(mouse_pos):
            self.switch_to_login_window()

    def register_user(self):
        if self.username and self.password and self.repeat_password:
            if self.password == self.repeat_password:

                data = {
                    "username": self.username,
                    "password": self.password,
                    "PLAYER_VS_COMPUTER": {
                        "games": [],
                        "last_save": {}
                    },
                    "PLAYER_VS_PLAYER_LOCAL": {
                        "games": [],
                    }
                }

                try:
                    print("[SERVER] Registering...")
                    response = requests.post("http://localhost:8080/register", json=data)
                    if response.status_code == 200:
                        print("[SERVER] User registered successfully!")
                        p.quit()
                        self.running = False

                        set_username(self.username)

                        print("[SERVER] You are logged in!")

                        ModeWindow().run()

                    else:
                        print("[SERVER] Failed to register user. Status code:", response.status_code)
                except requests.exceptions.RequestException as e:
                    print("[SERVER] Error occurred during the request:", str(e))

            else:
                print("[SERVER] Passwords do not match.")
        else:
            print("[SERVER] Please fill in all fields.")

    def switch_to_login_window(self):
        self.running = False
        p.quit()
        from app.GUI.Auth.LoginWindow import LoginWindow
        print("[SERVER] Switching to login window")
        LoginWindow().run()

    def draw(self):

        self.screen.fill(self.white)

        p.draw.rect(self.screen, self.gray,
                    (self.input_box_x + 15, self.input_box_y - 100, self.input_box_width, self.input_box_height), 2)
        p.draw.rect(self.screen, self.gray,
                    (self.input_box_x + 15, self.input_box_y - 20, self.input_box_width, self.input_box_height), 2)
        p.draw.rect(self.screen, self.gray,
                    (self.input_box_x + 15, self.input_box_y + 60, self.input_box_width, self.input_box_height), 2)

        username_label = self.font1.render("Username:", True, self.black)
        username_label_rect = username_label.get_rect(center=(self.input_box_x - 50, self.input_box_y - 80))
        self.screen.blit(username_label, username_label_rect)

        password_label = self.font1.render("Password:", True, self.black)
        password_label_rect = password_label.get_rect(center=(self.input_box_x - 50, self.input_box_y))
        self.screen.blit(password_label, password_label_rect)

        repeat_password_label = self.font1.render("Repeat pwd:", True, self.black)
        repeat_password_label_rect = repeat_password_label.get_rect(
            center=(self.input_box_x - 50, self.input_box_y + 80))
        self.screen.blit(repeat_password_label, repeat_password_label_rect)

        self.screen.blit(self.font1.render(self.username, True, self.black),
                         (self.input_box_x + 24, self.input_box_y - 92))
        self.screen.blit(self.font1.render("*" * len(self.password), True, self.black),
                         (self.input_box_x + 24, self.input_box_y - 8))
        self.screen.blit(self.font1.render("*" * len(self.repeat_password), True, self.black),
                         (self.input_box_x + 24, self.input_box_y + 72))

        p.draw.rect(self.screen, self.green, (self.register_button_x + 15, self.register_button_y + 40,
                                              self.register_button_width, self.register_button_height))
        register_button_label = self.font1.render("Register", True, self.black)
        register_button_label_rect = register_button_label.get_rect(center=(self.width // 2 + 18,
                                                                            self.register_button_y + 58))
        self.screen.blit(register_button_label, register_button_label_rect)

        p.draw.rect(self.screen, self.gray, (self.login_button_x, self.login_button_y,
                                             self.login_button_width, self.login_button_height))
        login_button_label = self.font2.render("Switch to Login", True, self.black)
        login_button_label_rect = login_button_label.get_rect(
            center=(self.login_button_x + self.login_button_width // 2,
                    self.login_button_y + self.login_button_height // 2))
        self.screen.blit(login_button_label, login_button_label_rect)

        p.display.flip()

    def run(self):

        while self.running:

            for event in p.event.get():

                if event.type == p.QUIT:
                    self.running = False
                    p.quit()

                elif event.type == p.KEYDOWN:
                    self.handle_input(event)

                elif event.type == p.MOUSEBUTTONDOWN:
                    self.handle_mouse_click()

            if self.running:
                self.draw()
                self.clock.tick(MAX_FRAMERATE)

        p.quit()
