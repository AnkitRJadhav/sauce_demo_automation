from playwright.sync_api import Page
from config.config import config

class LoginPage:
    def __init__(self, page: Page):
        self.page = page

    def login(self, username, password):
        self.page.goto(config.BASE_URL)
        self.page.fill("#user-name", username)
        self.page.fill("#password", password)
        self.page.click("#login-button")
