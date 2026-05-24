from apscheduler.schedulers.blocking import BlockingScheduler
import datetime

def run_crawler():
    print("Bắt đầu cào dữ liệu:", datetime.datetime.now())
    # gọi hàm crawler + normalize ở đây
    # ví dụ: run_school_pipeline()

scheduler = BlockingScheduler()

# chạy 5 lần mỗi ngày, ví dụ cách nhau 4 tiếng
scheduler.add_job(run_crawler, 'cron', hour='0,4,8,12,16')

print("Scheduler đang chạy, sẽ cào 5 lần/ngày...")
scheduler.start()
