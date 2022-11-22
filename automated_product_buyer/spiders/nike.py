import scrapy
from scrapy import Request
from scrapy_playwright.page import PageMethod


def should_abort_request(req):
    if req.resource_type == "image":
        return True

    return False


class NikeSpider(scrapy.Spider):
    name = 'nike'
    allowed_domains = ['www.nike.com']
    start_urls = ['http://www.nike.com/']

    custom_settings = {
        # 'USER_AGENT': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.75 Safari/537.36',
        'USER_AGENT': None,
        # 'PLAYWRIGHT_ABORT_REQUEST': should_abort_request
    }

    def parse(self, response, *args, **kwargs):
        if 'playwright' not in response.meta:
            size = kwargs['size']
            yield Request(
                response.url,
                meta={
                    'playwright': True,
                    'playwright_include_page': True,
                    'playwright_page_methods': [
                        PageMethod('wait_for_selector', '[data-pre="LanguageMenu"]'),
                        PageMethod('click', '[data-pre="LanguageMenu"] .hf-modal-btn-close'),
                        PageMethod('wait_for_selector', f'//input[contains(@value,":{size}")]//parent::div'),
                        PageMethod('wait_for_timeout', 5000),
                        PageMethod('click', f'//input[contains(@value,":{size}")]//parent::div'),
                        PageMethod('wait_for_timeout', 5000),
                        PageMethod('wait_for_selector', '.add-to-cart-btn'),
                        PageMethod('wait_for_timeout', 5000),
                        PageMethod('click', '.add-to-cart-btn'),
                        # PageMethod('wait_for_timeout', 5000),
                        # PageMethod('wait_for_selector', '#nav-cart a'),
                        # PageMethod('click', '#nav-cart a'),
                        PageMethod('wait_for_timeout', 20000),
                    ],
                    'errback': self.errback,
                },
                callback=self.parse_product,
                dont_filter=True
            )

    async def parse_product(self, response, *args, **kwargs):
        page = response.meta["playwright_page"]
        await page.close()

        # return response.follow(
        #     response.css('#nav-cart a::attr(href)').get(),
        #     meta={
        #         'playwright': True,
        #         'playwright_include_page': True,
        #         'playwright_page_methods': [],
        #         'errback': self.errback,
        #     },
        #     callback=self.parse_cart,
        # )

    def parse_cart(self, *args, **kwargs):
        pass

    async def errback(self, failure):
        page = failure.request.meta["playwright_page"]
        await page.close()
