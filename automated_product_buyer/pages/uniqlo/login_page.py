from automated_product_buyer.pages.base_page import BasePage


class LoginPage(BasePage):
    url = 'https://www.uniqlo.com/us/auth/v1/login'

    def type_email(self, email):
        email_selector = 'input[type="email"]'
        self.type_input(email_selector, email)

    def type_password(self, password):
        password_selector = 'input[type="password"]'
        self.type_input(password_selector, password)

    def submit(self):
        submit_selector = '[data-test="login-button"]'
        locator = self.page.locator(submit_selector)
        self.click(locator)

    def login(self, email, password):
        self.type_email(email)
        self.type_password(password)
        self.submit()
