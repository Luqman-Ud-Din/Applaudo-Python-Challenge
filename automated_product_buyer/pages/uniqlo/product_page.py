from automated_product_buyer.pages.base_page import BasePage


class ProductPage(BasePage):
    def click_add_to_cart(self):
        selector = 'button:text("Add to cart")'
        locator = self.page.locator(selector)
        self.click(locator)

    def click_view_cart(self):
        selector = 'button:text("View cart")'
        locator = self.page.locator(selector)
        self.click(locator)

    def click_checkout(self):
        selector = 'button:text("Checkout")'
        locator = self.page.locator(selector)
        self.click(locator)
