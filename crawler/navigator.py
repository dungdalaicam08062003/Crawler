KEYWORDS = {

    "tuition": [
        "học phí",
        "tuition",
        "chi phí"
    ],

    "admission": [
        "tuyển sinh",
        "xét tuyển",
        "admission"
    ]
}


async def find_related_links(page, category):

    results = []

    links = await page.locator("a").all()

    for link in links:

        try:

            text = await link.inner_text()

            href = await link.get_attribute("href")

            if not text or not href:
                continue

            text = text.strip()

            for keyword in KEYWORDS[category]:

                if keyword.lower() in text.lower():

                    results.append({
                        "text": text,
                        "href": href
                    })

        except:
            pass

    return results