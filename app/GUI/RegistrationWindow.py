import pygame as p
import requests
class RegistrationWindow:

    def __init__(self):

        p.init()
        self.width, self.height = 800, 600
        self.screen = p.display.set_mode((self.width, self.height))
        self.message_screen = None
        p.display.set_caption("Registration Window")

        self.white = (255, 255, 255)
        self.black = (0, 0, 0)
        self.gray = (128, 128, 128)
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

    def run(self):
        while self.running:
            for event in p.event.get():
                if event.type == p.QUIT:
                    self.running = False
                elif event.type == p.KEYDOWN:
                    if event.key == p.K_RETURN:
                        self.register_user()
                    elif event.key == p.K_BACKSPACE:
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

                elif event.type == p.MOUSEBUTTONDOWN:
                    mouse_pos = p.mouse.get_pos()

                    input_box_username_rect = p.Rect(self.input_box_x, self.input_box_y - 135, self.input_box_width,
                                                     self.input_box_height)
                    input_box_password_rect = p.Rect(self.input_box_x, self.input_box_y - 55, self.input_box_width,
                                                     self.input_box_height)
                    input_box_repeat_password_rect = p.Rect(self.input_box_x, self.input_box_y + 25, self.input_box_width,
                                                     self.input_box_height)
                    register_button_rect = p.Rect(self.register_button_x, self.register_button_y, self.register_button_width,
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
                        self.running = False
                        from app.GUI.LoginWindow import LoginWindow
                        LoginWindow().run()
                        print("Switching to login window")

            self.screen.fill(self.white)

            p.draw.rect(self.screen, self.gray,
                        (self.input_box_x, self.input_box_y - 135, self.input_box_width, self.input_box_height), 2)
            p.draw.rect(self.screen, self.gray, (self.input_box_x, self.input_box_y - 55, self.input_box_width, self.input_box_height), 2)
            p.draw.rect(self.screen, self.gray,
                        (self.input_box_x, self.input_box_y + 25, self.input_box_width, self.input_box_height), 2)

            username_label = self.font1.render("Username:", True, self.black)
            username_label_rect = username_label.get_rect(center=(self.input_box_x - 100, self.input_box_y - 120))
            self.screen.blit(username_label, username_label_rect)

            password_label = self.font1.render("Password:", True, self.black)
            password_label_rect = password_label.get_rect(center=(self.input_box_x - 100, self.input_box_y - 40))
            self.screen.blit(password_label, password_label_rect)

            repeat_password_label = self.font1.render("Repeat Password:", True, self.black)
            repeat_password_label_rect = repeat_password_label.get_rect(center=(self.input_box_x - 100, self.input_box_y + 40))
            self.screen.blit(repeat_password_label, repeat_password_label_rect)

            self.screen.blit(self.font1.render(self.username, True, self.black), (self.input_box_x + 7, self.input_box_y - 128))
            self.screen.blit(self.font1.render("*" * len(self.password), True, self.black), (self.input_box_x + 7, self.input_box_y - 43))
            self.screen.blit(self.font1.render("*" * len(self.repeat_password), True, self.black), (self.input_box_x + 7, self.input_box_y + 37))

            register_button = p.Rect(self.register_button_x, self.register_button_y, self.register_button_width, self.register_button_height)
            p.draw.rect(self.screen, self.gray, register_button, 2)
            self.screen.blit(self.font1.render("Register", True, self.black), (self.register_button_x + 60, self.register_button_y + 7))

            if self.input_active == "username":
                p.draw.rect(self.screen, self.green, (self.input_box_x - 3, self.input_box_y - 138, self.input_box_width + 6, self.input_box_height + 6), 3)
            elif self.input_active == "password":
                p.draw.rect(self.screen, self.green, (self.input_box_x - 3, self.input_box_y - 58, self.input_box_width + 6, self.input_box_height + 6), 3)
            elif self.input_active == "repeat_password":
                p.draw.rect(self.screen, self.green, (self.input_box_x - 3, self.input_box_y + 22, self.input_box_width + 6, self.input_box_height + 6), 3)

            p.draw.rect(self.screen, self.gray,
                        (self.login_button_x, self.login_button_y, self.login_button_width, self.login_button_height))
            login_text = self.font2.render("Already have an account? Log in", True, self.black)
            login_text_rect = login_text.get_rect(center=(
            self.login_button_x + self.login_button_width // 2, self.login_button_y + self.login_button_height // 2))
            self.screen.blit(login_text, login_text_rect)

            p.display.flip()

        p.quit()

    def display_message(self, message):
        self.message_screen = p.display.set_mode((400, 200))
        self.message_screen.fill(self.white)
        text = self.font1.render(message, True, self.black)
        text_rect = text.get_rect(center=(self.message_screen.get_width() // 2, self.message_screen.get_height() // 2))

    def register_user(self):
        if self.username and self.password and self.repeat_password:
            if self.password == self.repeat_password:
                # print("Username:", self.username)
                # print("Password:", self.password)

                # POSTING NEW USER

                data = {
                    "username": self.username,
                    "password": self.password,
                    "pvComputer": [],
                    "pvpLocal": [],
                    "pvpOnline": []
                }

                try:
                    response = requests.post("http://localhost:8080/register", json=data)
                    if response.status_code == 200:
                        print("User registered successfully!")
                        self.running = False

                    else:
                        print("Failed to register user. Status code:", response.status_code)
                except requests.exceptions.RequestException as e:
                    print("Error occurred during the request:", str(e))

            else:
                print("Passwords do not match.")
                # self.display_message("Passwords do not match!")
        else:
            print("Please fill in all fields.")
            # self.display_message("Please fill in all fields!")


# RegistrationWindow().run()