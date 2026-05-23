from playwright.async_api import async_playwright
from normalize import normalize_article

import asyncio


URL = "https://tuyensinh.vku.udn.vn/thong-bao/69af03ade1fedb5e0308e873"


async def main():

    async with async_playwright() as p:

        browser = await p.chromium.launch(
            headless=True,
            args=[
                "--no-sandbox",
                "--disable-dev-shm-usage"
            ]
        )

        page = await browser.new_page()

        await page.goto(URL)

        await page.wait_for_timeout(3000)

        raw_data = {

            "title": await page.locator("h1").inner_text(),

            "content": await page.locator("body").inner_text(),

            "url": page.url
        }

        normalized = normalize_article(raw_data)

        print(normalized)

        await browser.close()


asyncio.run(main())