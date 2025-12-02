import time

from playwright.sync_api import Page

class CheckoutPage:
    def __init__(self, page: Page):
        self.page = page

    def complete_checkout(self, first_name, last_name, postal_code):
        self.page.fill("[data-test='firstName']", first_name)
        self.page.fill("[data-test='lastName']", last_name)
        self.page.fill("[data-test='postalCode']", postal_code)
        self.page.click("[data-test='continue']")
        self.page.click("[data-test='finish']")

    def get_order_confirmation_message(self):
        self.page.wait_for_selector(".complete-header")
        return self.page.text_content(".complete-header")
