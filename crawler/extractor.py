async def extract_content(page):

    title = await page.title()

    content = await page.locator("body").inner_text()

    html = await page.locator("body").inner_html()

    return {

        "title": title,

        "content": content,

        "html": html,

        "url": page.url
    }