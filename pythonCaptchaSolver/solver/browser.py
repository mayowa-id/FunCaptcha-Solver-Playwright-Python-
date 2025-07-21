from playwright.sync_api import sync_playwright
import time

class BrowserManager:
    def __init__(self, headless=True):
        self.playwright = sync_playwright().start()
        self.browser = self.playwright.chromium.launch(headless=headless)
        self.context = self.browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64)...",
            locale="en-US"
        )
        self.page = self.context.new_page()

    def goto(self, url):
        self.page.goto(url, wait_until="networkidle")
        time.sleep(2)  # simulate human delay

    def close(self):
        self.context.close()
        self.browser.close()
        self.playwright.stop()
