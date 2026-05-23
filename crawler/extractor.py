async def extract_content(page):

    title = await page.title()

    content = await page.locator("body").inner_text()

    return {
        "title": title,
        "content": content[:1500],
        "url": page.url
    }