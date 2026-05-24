from fastapi import FastAPI, HTTPException
import os, json

app = FastAPI()

OUTPUT_DIR = "output"

@app.get("/data/{school}")
def get_school_data(school: str):
    """
    Trả về dữ liệu JSON đã chuẩn hóa cho một trường cụ thể.
    Ví dụ: /data/vku sẽ trả về nội dung file vku_normalized.json
    """
    filename = f"{school}_normalized.json"
    filepath = os.path.join(OUTPUT_DIR, filename)

    if not os.path.exists(filepath):
        raise HTTPException(status_code=404, detail="File không tồn tại")

    with open(filepath, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data

@app.get("/data/all")
def get_all_data():
    """
    Trả về dữ liệu của tất cả các trường đã chuẩn hóa.
    """
    results = {}
    for file in os.listdir(OUTPUT_DIR):
        if file.endswith("_normalized.json"):
            school = file.replace("_normalized.json", "")
            with open(os.path.join(OUTPUT_DIR, file), "r", encoding="utf-8") as f:
                results[school] = json.load(f)
    return results
