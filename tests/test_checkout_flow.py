import pytest
from playwright.sync_api import sync_playwright, Page
from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage
from pages.cart_page import CartPage
from pages.checkout_page import CheckoutPage
from config.config import config


@pytest.fixture(scope="function")
def page() -> Page:
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context()
        page = context.new_page()
        yield page
        context.close()
        browser.close()


@pytest.mark.checkout
def test_successful_checkout_flow(page: Page):
    login_page = LoginPage(page)
    inventory_page = InventoryPage(page)
    cart_page = CartPage(page)
    checkout_page = CheckoutPage(page)

    first_name = "Ankit"
    last_name = "Jadhav"
    postal_code = "411057"

    login_page.login(config.VALID_USERNAME, config.VALID_PASSWORD)
    assert "inventory.html" in page.url, "Login failed."
    print("Logged in successfully")

    added_items = inventory_page.add_random_items_to_cart(num_items=3)
    print("Added items: ", added_items)
    assert len(added_items) == 3, "Did not add expected number of items."
    assert inventory_page.get_cart_item_count() == 3, "Cart badge count incorrect."
    print("Items successfully added to cart")

    inventory_page.go_to_cart()
    assert "cart.html" in page.url, "Failed to go to cart."
    items_in_cart = cart_page.get_cart_item_names()
    print("Items in cart: ", items_in_cart)
    assert len(items_in_cart) == 3, "Incorrect number of items in cart."
    for item in added_items:
        assert item in items_in_cart, f"Item '{item}' missing from cart."

    cart_page.click_checkout()
    assert "checkout-step-one.html" in page.url, "Failed to start checkout."
    checkout_page.complete_checkout(first_name, last_name, postal_code)
    assert "checkout-complete.html" in page.url, "Checkout process failed."

    confirmation_message = checkout_page.get_order_confirmation_message()
    print("Confirmation message: ", confirmation_message)
    assert "Thank you for your order!" in confirmation_message, "Order confirmation not found."

