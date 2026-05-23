async def extract_content(page):

    title = await page.title()

    content = await page.locator("body").inner_text()

    html = await page.locator("body").inner_html()

    tables = await page.locator("table").all_inner_texts()

    links = await page.locator("a").evaluate_all(
        """
        elements => elements.map(a => ({
            text: a.innerText,
            href: a.href
        }))
        """
    )

    return {
        "title": title,
        "content": content,
        "html": html,
        "tables": tables,
        "links": links,
        "url": page.url
    }