from playwright.async_api import async_playwright

from config import HEADLESS


class BrowserEngine:

    async def start(self):

        self.playwright = await async_playwright().start()

        self.browser = await self.playwright.chromium.launch(
            headless=HEADLESS,
            args=[
                "--no-sandbox",
                "--disable-dev-shm-usage"
            ]
        )

    async def new_page(self):

        return await self.browser.new_page()

    async def close(self):

        await self.browser.close()

        await self.playwright.stop()