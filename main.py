from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from hoverable import HoverBehavior
import json
from kivy.uix.image import Image
from kivy.uix.behaviors import ButtonBehavior
from datetime import datetime
import random
import os

Builder.load_file('design.kv')


class LoginScreen(Screen):

    def sign_up(self):

        self.manager.transition.direction = "left"
        self.manager.current = "sign_up_screen"

    def log_in(self, username, password):

        with open("users.json", 'r') as file:
            users = json.load(file)

        if username and password:

            if username in users.keys():

                if password == users[username]['password']:

                    self.manager.transition.direction = "left"
                    self.manager.current = "logged_in_screen"

                else:

                    self.ids.failed_login.text = "Incorrect password!"

            else:

                self.ids.failed_login.text = "incorrect username!"

        else:
            self.ids.failed_login.text = "Username and password must not be blank."

    def frgt_pswd(self):
        self.manager.transition.direction = "left"
        self.manager.current = "forgot_pswd_scrn"


class RootWidget(ScreenManager):

    pass


class SignUpScreen(Screen):

    def add_user(self, uname, pswd):

        if uname and pswd:

            with open("users.json", 'r') as file:

                users = json.load(file)

            if uname not in users.keys():

                users[uname] = {'username': uname, 'password': pswd,
                                'created': datetime.now().strftime("%Y-%m-%d %H-%M-%S")}

                with open("users.json", 'w') as file:
                    json.dump(users, file)
                self.manager.current = "success_screen"
            else:
                self.ids.err_msg.text = "This username already exists please try logging in."

        else:
            self.ids.err_msg.text = "Username and password fields must not be empty."

    def get_back(self):

        self.manager.transition.direction = "right"
        self.manager.current = "login_screen"

class SuccessScreen(Screen):

    def get_back(self):

        self.manager.transition.direction = "right"
        self.manager.current = "login_screen"


class ForgotpswdScrn(Screen):
    def reset_pswd(self, username, new_pswd, new_pswd_conf):
        with open("users.json", 'r') as file:
            users = json.load(file)

        if username and new_pswd and new_pswd_conf:

            if username in users.keys():

                if new_pswd_conf == new_pswd:

                    users[username]['password'] = new_pswd
                    with open("users.json", 'w') as file:
                        json.dump(users, file)
                    self.manager.current = "success_screen"

                else:
                    self.ids.wrng_uname.text = "The confirmed password is not same as the entered password!"

            else:
                self.ids.wrng_uname.text = "This username doesn't exist."

        else:
            self.ids.wrng_uname.text = "Username and password fields must not be empty."

    def get_back(self):

        self.manager.transition.direction = "right"
        self.manager.current = "login_screen"




class ChangedpswdScreen(Screen):
    def get_back(self):

        self.manager.transition.direction = "right"
        self.manager.current = "login_screen"

    


class LoggedInScreen(Screen):

    def log_out(self):

        self.manager.transition.direction = "right"
        self.manager.current = "login_screen"

    def get_quote(self, feeling):

        if feeling:

            feeling = feeling.lower()

            if os.path.exists(f'quotes\{feeling}.txt'):

                with open(f'quotes\{feeling}.txt', 'r', encoding="utf8") as file:

                    quote_out = file.read().splitlines()

                self.ids.quote.text = random.choice(quote_out)

            else:

                self.ids.quote.text = "We don't have any quotes for your current mood please try any other mood."

        else:

            self.ids.quote.text = "Please specify your mood !"

class ImageButton(ButtonBehavior, HoverBehavior, Image):
    pass


class MainApp(App):

    def build(self):

        return RootWidget()


if __name__ == '__main__':
    MainApp().run()
