from crawler.playwright_engine import BrowserEngine

from crawler.navigator import find_related_links

from crawler.extractor import extract_content

from models.school_model import SchoolData

from utils.logger import log_step

from config import VKU_URL


async def run_school_pipeline():

    browser_engine = BrowserEngine()

    await browser_engine.start()

    page = await browser_engine.new_page()

    # STEP 1

    log_step("STEP 1: OPEN SCHOOL PAGE")

    await page.goto(VKU_URL)

    await page.wait_for_load_state("networkidle")

    print("Current URL:", page.url)

    # STEP 2

    log_step("STEP 2: FIND TUITION LINKS")

    tuition_links = await find_related_links(
        page,
        "tuition"
    )

    print(tuition_links)

    # STEP 3

    log_step("STEP 3: FIND ADMISSION LINKS")

    admission_links = await find_related_links(
        page,
        "admission"
    )

    print(admission_links)

    # STEP 4

    log_step("STEP 4: EXTRACT CONTENT")

    extracted = await extract_content(page)

    # STEP 5

    log_step("STEP 5: CREATE MODEL")

    school_data = SchoolData(

        title=extracted["title"],

        url=extracted["url"],

        content=extracted["content"],

        tuition_links=tuition_links,

        admission_links=admission_links
    )

    print(school_data.to_dict())

    await browser_engine.close()