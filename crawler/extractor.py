async def extract_content(page):

    title = await page.title()

    content = await page.locator("body").inner_text()

    return {

        "title": title,

        "content": content[:2000],

        "url": page.url
    }