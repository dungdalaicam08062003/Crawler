import asyncio
import threading
import uvicorn
from apscheduler.schedulers.background import BackgroundScheduler

# import API app từ file api.py
from api import app
from pipeline.school_pipeline import run_school_pipeline
from normalized.nomalized import normalized
from config import VKU_URL, UDN_URL, UED_URL, DUT_URL, DUE_URL, UFL_URL, UTE_URL, SMP_URL

# Hàm async pipeline
async def code_run_async(specification):
    await run_school_pipeline(specification[0])
    if await normalized(specification[1]):
        print(f"✅ Pipeline {specification[1]} completed successfully.")

# Hàm sync để scheduler gọi
def code_run(specification):
    asyncio.run(code_run_async(specification))

# Khởi tạo scheduler chạy song song
scheduler = BackgroundScheduler()
scheduler.add_job(code_run, 'cron', hour=0, args=[VKU_URL])
scheduler.add_job(code_run, 'cron', hour=1, args=[UDN_URL])
scheduler.add_job(code_run, 'cron', hour=2, args=[UED_URL])
scheduler.add_job(code_run, 'cron', hour=3, args=[DUT_URL])
scheduler.add_job(code_run, 'cron', hour=4, args=[DUE_URL])
scheduler.add_job(code_run, 'cron', hour=5, args=[UFL_URL])
scheduler.add_job(code_run, 'cron', hour=6, args=[UTE_URL])
scheduler.add_job(code_run, 'cron', hour=7, args=[SMP_URL])
scheduler.start()

# Chạy API trong thread riêng
def run_api():
    uvicorn.run(app, host="localhost", port=8000)

if __name__ == "__main__":
    # Tạo thread cho API
    api_thread = threading.Thread(target=run_api, daemon=True)
    api_thread.start()

    print("✅ Scheduler và API đang chạy song song... (Ctrl+C để dừng)")
    # Giữ tiến trình chính sống
    try:
        while True:
            pass
    except KeyboardInterrupt:
        print("⏹ Dừng hệ thống")
