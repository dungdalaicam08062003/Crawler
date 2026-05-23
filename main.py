import asyncio

from crawler.google_search import search_school
from crawler.navigator import find_related_links
from crawler.extractor import extract_content


async def main():

    print("STEP 1: Search VKU")

    result = await search_school(
        "VKU official website"
    )

    print(result["title"])
    print(result["link"])

    browser = result["browser"]

    page = await browser.new_page()

    await page.goto(result["link"])

    print()

    print("STEP 2: Find tuition information")

    tuition_links = await find_related_links(
        page,
        "tuition"
    )

    print(tuition_links)

    print()

    print("STEP 3: Find admission information")

    admission_links = await find_related_links(
        page,
        "admission"
    )

    print(admission_links)

    if tuition_links:

        first_link = tuition_links[0]["href"]

        await page.goto(first_link)

        data = await extract_content(page)

        print()

        print("=== TUITION CONTENT ===")

        print(data)

    await browser.close()


asyncio.run(main())