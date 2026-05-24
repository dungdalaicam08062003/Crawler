import json
import re
import os
import google.generativeai as genai

async def normalized(filename):
    try:
        genai.configure(api_key="AIzaSyBKRKXXkSbC3ekgkFOnRcE9AGqaxwvS8QU")
        path = os.path.join("output", "file_data.json")
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)

        model = genai.GenerativeModel("gemini-2.5-flash")

        prompt = f"""
        Bạn hãy chuẩn hóa dữ liệu sau thành JSON sạch và ngắn gọn.

        Yêu cầu:
        - Chỉ trả về JSON hợp lệ.
        - Format nhiều dòng (pretty print).
        - Có thể lưu trực tiếp thành file `.json`.
        - Bỏ qua dữ liệu dư thừa như: html, script, css, navigation, banner, footer,...
        - Chỉ giữ các thông tin chính như:
        university_name, address, phone, email, website, description, majors, tuition, images,...
        - Không thêm giải thích hay text ngoài JSON.
        - Không tạo các field như:
        normalized_raw,
        analysis,
        explanation

        Ví dụ output đúng:
        {{
        "university_name": "Đại học VKU",
        "address": "Đà Nẵng",
        "website": "https://vku.udn.vn",
        "email": "contact@vku.udn.vn"
        }}
        lưu ý cái này chỉ là ví dụ hãy dynamic để đủ dữ liệu 
        Dữ liệu:
        {json.dumps(data, ensure_ascii=False)}
        """

        response = model.generate_content(prompt)

        normalized_text = response.text.strip()

        # Xóa markdown ```json
        normalized_text = re.sub(r"^```json", "", normalized_text)
        normalized_text = re.sub(r"^```", "", normalized_text)
        normalized_text = re.sub(r"```$", "", normalized_text)
        normalized_text = normalized_text.strip()

        try:
            normalized_data = json.loads(normalized_text)

            with open(f"output/{filename}_normalized.json", "w", encoding="utf-8") as f:
                json.dump(normalized_data, f, ensure_ascii=False, indent=2)

            print("✅ Đã chuẩn hóa thành công")

        except Exception as e:
            print("❌ JSON không hợp lệ")
            print(e)

            with open("output/error_response.txt", "w", encoding="utf-8") as f:
                f.write(normalized_text)
        return 1
    except Exception as e:
        return 0

    
