import json

import scrapy
from playwright.sync_api import sync_playwright
from playwright_stealth import stealth_sync
from scrapy import Request

from automated_product_buyer.helpers import strip_text, should_abort_image_requests
from automated_product_buyer.pages.uniqlo.cart_page import CartPage
from automated_product_buyer.pages.uniqlo.checkout_delivery_page import CheckoutDeliveryPage
from automated_product_buyer.pages.uniqlo.checkout_payment_page import CheckoutPaymentPage
from automated_product_buyer.pages.uniqlo.login_page import LoginPage
from automated_product_buyer.pages.uniqlo.product_page import ProductPage


class ProductParser:
    def parse_product_color(self, response):
        color_css = '#product-color-picker [checked]::attr(aria-label)'
        value_css = '#product-color-picker [checked]::attr(value)'
        color = next(iter(strip_text(response.css(color_css).extract())), None)
        value = next(iter(strip_text(response.css(value_css).extract())), None)
        return ' '.join(strip_text([value, color]))

    def parse_product_size(self, response):
        size_css = '#product-size-picker [checked]::attr(aria-label)'
        return next(iter(strip_text(response.css(size_css).extract())), None)

    def parse_product_name(self, response):
        return next(iter(strip_text(response.css('h1.fr-ec-display::text').extract())), None)

    def parse(self, response, *args, **kwargs):
        return {
            'url': response.url,
            'color': self.parse_product_color(response),
            'size': self.parse_product_size(response),
            'name': self.parse_product_name(response)
        }


class CheckoutParser:
    def parse_delivery_subtotal(self, response):
        subtotal_xpath = '//td[contains(., "Subtotal")]//parent::*/td[2]//text()'
        return next(iter(strip_text(response.xpath(subtotal_xpath).extract())), None)

    def parse_delivery_shipping_cost(self, response):
        shipping_cost_xpath = '//td[contains(., "Shipping")]//parent::*/td[2]//text()'
        return next(iter(strip_text(response.xpath(shipping_cost_xpath).extract())), None)

    def parse_delivery_estimated_tax(self, response):
        estimated_tax_xpath = '//td[contains(., "Estimated Tax")]//parent::*/td[2]//text()'
        return next(iter(strip_text(response.xpath(estimated_tax_xpath).extract())), None)

    def parse_delivery_total(self, response):
        total_xpath = '//td[contains(., "Order total")]//parent::*/td[2]//text()'
        return next(iter(strip_text(response.xpath(total_xpath).extract())), None)

    def parse_delivery_shipping_option(self, response):
        shipping_option_xpath = '//p[contains(text(), "Shipping speed option:")]//text()'
        shipping_option_re = 'Shipping speed option: (.*)'
        return next(iter(strip_text(response.xpath(shipping_option_xpath).re(shipping_option_re))), None)

    def parse_estimated_delivery_date(self, response):
        delivery_date_xpath = '//p[contains(text(), "Estimated delivery time:")]//text()'
        delivery_date_re = 'Estimated delivery time: (.*)'
        return next(iter(strip_text(response.xpath(delivery_date_xpath).re(delivery_date_re))), None)

    def parse(self, response, *args, **kwargs):
        return {
            'subtotal': self.parse_delivery_subtotal(response),
            'shipping_cost': self.parse_delivery_shipping_cost(response),
            'estimated_tax': self.parse_delivery_estimated_tax(response),
            'total': self.parse_delivery_total(response),
            'shipping_option': self.parse_delivery_shipping_option(response),
            'estimated_shipping_date': self.parse_estimated_delivery_date(response)
        }


class UniqloSpider(scrapy.Spider):
    name = 'uniqlo'
    allowed_domains = ['www.uniqlo.com']

    product_parser = ProductParser()
    checkout_parser = CheckoutParser()

    def __init__(self, product_url='', profile_information='{}', *arg, **kwargs):
        super().__init__(**kwargs)
        self.product_url = product_url
        self.profile_information = json.loads(profile_information)

    def start_requests(self):
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            stealth_sync(page)
            page.route("**/*", should_abort_image_requests)

            checkout_payment_page = CheckoutPaymentPage(page)
            checkout_payment_page.open()

            login_page = LoginPage(page)
            login_page.login('luqmanuddinm@gmail.com', 'test1234')

            cart_page = CartPage(page)
            cart_page.open()
            cart_page.remove_items()

            product_page = ProductPage(page)
            product_page.url = self.product_url
            product_page.open()

            product_response = product_page.to_response()
            product_page.click_add_to_cart()

            checkout_payment_page.open()
            checkout_payment_page.click_change_delivery_option()

            checkout_delivery_page = CheckoutDeliveryPage(page)
            checkout_delivery_page.click_ship_to_address()
            checkout_delivery_page.click_edit_address()
            checkout_delivery_page.populate_address(self.profile_information)
            checkout_delivery_page.click_register_address()
            checkout_delivery_page.click_continue_selected_delivery_option()
            checkout_delivery_page.click_continue_selected_delivery_option()

            checkout_response = checkout_payment_page.to_response()
            browser.close()
            return [self.create_scrapy_request(checkout_response, product_response)]

    def parse(self, response, *args, **kwargs):
        product = response.meta['product']
        checkout = self.checkout_parser.parse(response)
        return {**product, **checkout}

    def create_scrapy_request(self, checkout_response, product_response):
        request = Request(
            checkout_response.url,
            dont_filter=True,
            meta={
                'custom_rendered_response': checkout_response,
                'product': self.product_parser.parse(product_response)
            },
            callback=self.parse
        )
        checkout_response.request = request

        return request
