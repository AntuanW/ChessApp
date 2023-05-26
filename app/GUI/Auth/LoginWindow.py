import pygame as p
import requests

from app.config import set_nick
from app.GUI.ModeWindow.ModeWindow import ModeWindow
from app.GUI.Auth.RegistrationWindow import RegistrationWindow


class LoginWindow:

    def __init__(self):
        p.init()
        self.width, self.height = 800, 600
        self.screen = p.display.set_mode((self.width, self.height))
        p.display.set_caption("Login Window")

        self.white = (255, 255, 255)
        self.black = (0, 0, 0)
        self.gray = (128, 128, 128)
        self.green = (0, 255, 0)

        self.font1 = p.font.SysFont("Arial", 20, bold=True)
        self.font2 = p.font.SysFont("Arial", 16, bold=True)

        self.username = ""
        self.password = ""
        self.input_box_width = 200
        self.input_box_height = 40
        self.input_box_x = self.width // 2 - self.input_box_width // 2
        self.input_box_y = self.height // 2 - self.input_box_height

        self.register_button_width = 270
        self.register_button_height = 30
        self.register_button_x = self.width - self.register_button_width - 20
        self.register_button_y = 40

        self.running = True
        self.input_active = ""

    def handle_input(self, event):
        if event.key == p.K_BACKSPACE:
            if self.username and self.input_active == "username":
                self.username = self.username[:-1]
            elif self.password and self.input_active == "password":
                self.password = self.password[:-1]
        else:
            if self.input_active == "username" and len(self.username) < 10:
                self.username += event.unicode
            elif self.input_active == "password" and len(self.password) < 10:
                self.password += event.unicode

    def handle_mouse_click(self):

        mouse_pos = p.mouse.get_pos()

        input_box_username_rect = p.Rect(self.input_box_x, self.input_box_y - 135, self.input_box_width,
                                         self.input_box_height)
        input_box_password_rect = p.Rect(self.input_box_x, self.input_box_y - 55, self.input_box_width,
                                         self.input_box_height)
        log_in_button_rect = p.Rect(self.input_box_x, self.input_box_y + 30, self.input_box_width,
                                    self.input_box_height)

        if input_box_username_rect.collidepoint(mouse_pos):
            self.input_active = "username"
        elif input_box_password_rect.collidepoint(mouse_pos):
            self.input_active = "password"
        elif log_in_button_rect.collidepoint(mouse_pos):
            self.log_in_user()
        else:
            self.input_active = ""

        register_button_rect = p.Rect(self.register_button_x, self.register_button_y,
                                      self.register_button_width, self.register_button_height)

        if register_button_rect.collidepoint(mouse_pos):
            self.switch_to_registration_window()

    def log_in_user(self):
        print("Username:", self.username)
        print("Password:", self.password)

        # CHECKING USER CREDENTIALS

        data = {
            "username": self.username,
            "password": self.password,
        }

        try:
            print("Logging in...")
            response = requests.post("http://localhost:8080/login", json=data)
            if response.status_code == 200:
                print("User logged in successfully!")
                p.quit()
                self.running = False

                print("saving username to global variable")
                set_nick(self.username)

                print("Switching to mode window")
                ModeWindow().run()

            else:
                print("Failed to log in user. Status code:", response.status_code)

        except requests.exceptions.RequestException as e:
            print("Error occurred during the request:", str(e))

    def switch_to_registration_window(self):
        self.running = False
        print("Switching to registration window")
        RegistrationWindow().run()

    def draw(self):
        self.screen.fill(self.white)

        p.draw.rect(self.screen, self.gray,
                    (self.input_box_x, self.input_box_y - 135, self.input_box_width, self.input_box_height), 2)
        p.draw.rect(self.screen, self.gray,
                    (self.input_box_x, self.input_box_y - 55, self.input_box_width, self.input_box_height), 2)

        username_label = self.font1.render("Username:", True, self.black)
        username_label_rect = username_label.get_rect(center=(self.input_box_x - 100, self.input_box_y - 120))
        self.screen.blit(username_label, username_label_rect)

        password_label = self.font1.render("Password:", True, self.black)
        password_label_rect = password_label.get_rect(center=(self.input_box_x - 100, self.input_box_y - 40))
        self.screen.blit(password_label, password_label_rect)

        self.screen.blit(self.font1.render(self.username, True, self.black), (self.input_box_x + 7, self.input_box_y - 128))
        self.screen.blit(self.font1.render("*" * len(self.password), True, self.black), (self.input_box_x + 7, self.input_box_y - 43))

        log_in_button = p.Rect(self.input_box_x, self.input_box_y + 30, self.input_box_width, self.input_box_height)
        p.draw.rect(self.screen, self.gray, log_in_button, 2)
        self.screen.blit(self.font1.render("Log in", True, self.black), (self.input_box_x + 72, self.input_box_y + 37))

        p.draw.rect(self.screen, self.gray, (self.register_button_x, self.register_button_y, self.register_button_width, self.register_button_height))
        register_text = self.font2.render("Don't have an account? Sign up!", True, self.black)
        register_text_rect = register_text.get_rect(center=(self.register_button_x + self.register_button_width // 2, self.register_button_y + self.register_button_height // 2))
        self.screen.blit(register_text, register_text_rect)

        if self.input_active == "username":
            p.draw.rect(self.screen, self.green, (self.input_box_x - 3, self.input_box_y - 138, self.input_box_width + 6, self.input_box_height + 6), 3)
        elif self.input_active == "password":
            p.draw.rect(self.screen, self.green, (self.input_box_x - 3, self.input_box_y - 58, self.input_box_width + 6, self.input_box_height + 6), 3)

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

        p.quit()

