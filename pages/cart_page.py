from playwright.sync_api import Page

class CartPage:
    def __init__(self, page: Page):
        self.page = page

    def get_cart_item_names(self):
        self.page.wait_for_selector(".cart_item")
        return [name.inner_text() for name in self.page.locator(".inventory_item_name").all()]

    def click_checkout(self):
        self.page.click("[data-test='checkout']")
