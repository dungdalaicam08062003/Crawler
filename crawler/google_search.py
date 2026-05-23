from playwright.async_api import async_playwright


async def search_school(keyword):

    playwright = await async_playwright().start()

    browser = await playwright.chromium.launch(
        headless=True
    )

    page = await browser.new_page()

    await page.goto("https://www.google.com")

    await page.fill("textarea", keyword)

    await page.keyboard.press("Enter")

    await page.wait_for_timeout(3000)

    first_result = page.locator("h3").first

    title = await first_result.inner_text()

    link = await first_result.locator("..").get_attribute("href")

    return {
        "title": title,
        "link": link,
        "browser": browser,
        "playwright": playwright
    }