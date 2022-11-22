from automated_product_buyer.pages.base_page import BasePage


class CheckoutDeliveryPage(BasePage):
    url = 'https://www.uniqlo.com/us/en/checkout/delivery'

    def is_current_page(self):
        return '/checkout/delivery' in self.page.url

    def wait_for_page(self):
        self.page.wait_for_url('**/checkout/delivery**')

    def click_ship_to_address(self):
        selector = '//p[contains(., "Ship to address")]//ancestor::button'
        locator = self.page.locator(selector)
        self.click(locator)

    def click_edit_address(self):
        selector = '//span[contains(., "Edit")]//ancestor::button'
        locator = self.page.locator(selector)
        self.click(locator)

    def type_first_name(self, first_name):
        self.type_input('#id-givenName', first_name)

    def type_last_name(self, last_name):
        self.type_input('#id-familyName', last_name)

    def type_street(self, address_street):
        self.type_input('#id-street1', address_street)

    def type_city(self, city):
        self.type_input('#id-city', city)

    def type_zip_code(self, zip_code):
        self.type_input('#id-postalCode', zip_code)

    def type_phone(self, phone):
        self.type_input('#id-phone', phone)

    def select_state(self, state_code):
        input_selector = 'select[name="state"]+div input'
        input_locator = self.page.locator(input_selector)
        self.click(input_locator)
        state_selector = f'[role="option"][value="{state_code}"]'
        state_locator = self.page.locator(state_selector)
        self.click(state_locator)
        # self.page.get_by_label('State').select_option(state_code)

    def populate_address(self, address):
        self.type_first_name(address.get('first_name') or 'first name')
        self.type_last_name(address.get('last_name') or 'last name')
        self.type_street(address.get('street') or 'address street')
        self.type_city(address.get('city') or 'city')
        self.select_state(address.get('state_code') or '')
        self.type_zip_code(address.get('zip_code') or '')
        self.type_phone(address.get('phone') or '')

    def click_register_address(self):
        selector = 'button:text("Register")'
        locator = self.page.locator(selector)
        self.click(locator)

    def click_continue_selected_delivery_option(self):
        selector = '#selectedDeliveryMethod button:text("Continue")'
        locator = self.page.locator(selector)
        self.click(locator)

