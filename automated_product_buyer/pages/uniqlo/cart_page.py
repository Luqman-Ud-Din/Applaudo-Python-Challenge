from automated_product_buyer.pages.base_page import BasePage


class CartPage(BasePage):
    url = 'https://www.uniqlo.com/us/en/cart'

    def open(self):
        super().open()
        dialog_selector = '[aria-labelledby="cartIntegrationPopup"]'
        try:
            self.page.wait_for_selector(dialog_selector, timeout=10000)
            self.page.locator('[aria-labelledby="cartIntegrationPopup"] button:text("Ok")').click()
        except:
            pass

    def remove_items(self):
        selector = 'button[role="link"][aria-label="Remove"]'
        try:
            self.page.wait_for_selector(selector, timeout=15000)
        except:
            pass

        remove_locator = self.page.locator(selector)
        for i in range(remove_locator.count() - 1, -1, -1):
            remove_locator.nth(i).click()
            remove_dialog_locator = self.page.locator('[aria-labelledby="delete_item"] button:text("Remove")')
            remove_dialog_locator.wait_for()
            remove_dialog_locator.click()
