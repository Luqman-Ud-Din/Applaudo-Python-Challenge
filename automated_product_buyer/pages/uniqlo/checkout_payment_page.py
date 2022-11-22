from automated_product_buyer.pages.base_page import BasePage


class CheckoutPaymentPage(BasePage):
    url = 'https://www.uniqlo.com/us/en/checkout/payment'

    def is_current_page(self):
        self.page.wait_for_load_state('networkidle')
        return '/checkout/payment' in self.page.url

    def wait_for_page(self):
        self.page.wait_for_url('**/checkout/payment/**')

    def click_change_delivery_option(self):
        selector = '//span[contains(., "Change")]//ancestor::button'
        locator = self.page.locator(selector)
        self.click(locator)
        self.click(self.page.locator('[role="dialog"] button:text("Edit")'))
