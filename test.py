import json
import asyncio
from config import SCHOOL_URLS

async def crawl_school(url, short_name):
    # Đây chỉ là ví dụ giả lập, thay bằng logic crawler thật của bạn
    data = {
        "school": short_name,
        "url": url,
        "info": f"Dữ liệu giả lập cho {short_name}"
    }

    filename = f"output/{short_name}_normalized.json"
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print(f"✅ Đã lưu {filename}")

async def run_school_pipeline():
    tasks = [crawl_school(url, short_name) for url, short_name in SCHOOL_URLS]
    await asyncio.gather(*tasks)
asyncio.run(run_school_pipeline())