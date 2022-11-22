import typing

from playwright.async_api import Page as AsyncPage
from playwright.sync_api import Page as SyncPage
from scrapy.http import TextResponse


class BasePage:
    url = ''

    def __init__(self, page: typing.Union[SyncPage, AsyncPage]):
        self.page = page

    def open(self):
        retries = 3
        for i in range(retries):
            print(f'trying {i + 1}: opening: ', self.url)
            try:
                self.page.goto(self.url)
                break
            except Exception as e:
                print(f'failed to load: ', self.url)
                if i == retries - 1:
                    raise e

    def to_response(self):
        try:
            self.page.wait_for_load_state('networkidle')
        except:
            pass
        return TextResponse(self.page.url, body=self.page.content(), encoding='utf-8')

    def click(self, locator):
        locator.wait_for()
        locator.scroll_into_view_if_needed()
        locator.click()

    def type_input(self, selector, text):
        locator = self.page.locator(selector)
        self.click(locator)
        locator.fill(text)
