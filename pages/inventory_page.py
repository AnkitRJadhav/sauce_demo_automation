import random
from playwright.sync_api import Page


class InventoryPage:
    def __init__(self, page: Page):
        self.page = page

    def add_random_items_to_cart(self, num_items=3):
        self.page.wait_for_selector(".inventory_item_name")
        product_elements = self.page.locator(".inventory_item_name").all()

        if len(product_elements) < num_items:
            raise ValueError("Not enough products.")

        items_to_add = random.sample(product_elements, num_items)
        added_names = []

        for item in items_to_add:
            name = item.inner_text()
            item_id = name.lower().replace(" ", "-")
            self.page.click(f"[data-test='add-to-cart-{item_id}']")
            added_names.append(name)

        return added_names

    def get_cart_item_count(self):
        if self.page.locator(".shopping_cart_badge").is_visible():
            return int(self.page.locator(".shopping_cart_badge").inner_text())
        return 0

    def go_to_cart(self):
        self.page.click(".shopping_cart_link")
