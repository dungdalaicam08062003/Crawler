import telebot
import g4f
import time
import re

TOKEN = "8978744018:AAG5rtbeoKbZsQAhyJGe8goGwI8iOCGM3Og"
bot = telebot.TeleBot(TOKEN)

user_histories = {}

# Đọc dữ liệu từ file kiến thức
try:
    with open("vku_knowledge.txt", "r", encoding="utf-8") as file:
        vku_data = file.read()
    print("[OK] Đã tải dữ liệu VKU.")
except FileNotFoundError:
    print("[LỖI] Không tìm thấy file vku_knowledge.txt!")
    vku_data = ""


# --- MÔ HÌNH TRẢ LỜI CỤC BỘ (LOCAL MODEL) TỐC ĐỘ CAO ---
def local_intent_matcher(text):
    text_lower = text.lower()
    
    # 1. Intent: Hỏi địa chỉ
    if re.search(r"(ở đâu|địa chỉ|vị trí|nằm ở|thành phố nào|chỗ nào)", text_lower):
        if re.search(r"(vku|việt hàn|viet han|trường)", text_lower):
            return "📍 **Trường Đại học VKU (Đại học Đà Nẵng)** có trụ sở duy nhất tại: Số 470 Trần Đại Nghĩa, P. Hòa Quý, Q. Ngũ Hành Sơn, TP. Đà Nẵng."
            
    # 2. Intent: Hỏi học phí
    if re.search(r"(học phí|tiền học|bao nhiêu tiền|1 tín|một tín|đóng bao nhiêu)", text_lower):
        return "💰 **Học phí VKU (Trường Công lập):**\n- Đơn giá: Khoảng 500.000 VNĐ / 1 tín chỉ.\n- Trung bình 1 học kỳ: 12.000.000 - 14.000.000 VNĐ."

    # 3. Intent: Chính sách hỗ trợ / Học bổng
    if re.search(r"(hỗ trợ|học bổng|tân sinh viên|chính sách|miễn giảm|ktx|ký túc xá)", text_lower):
        return """🎁 **Chính sách hỗ trợ tân sinh viên VKU:**
- Miễn 100% học phí (2 kỳ đầu) cho ngành Vi mạch/Fintech (Điểm >=27).
- Miễn 50% học phí (2 kỳ đầu) cho điểm >=26 hoặc có Thư giới thiệu của Hiệu trưởng.
- Miễn phí 100% Ký túc xá (kỳ đầu) cho diện giảm học phí. KTX bình thường cực rẻ chỉ ~150k/tháng."""

    # 4. Intent: Sửa lỗi chính tả tên ngành riêng lẻ
    if re.search(r"(logistic|logictic|lô gic tich|chuỗi cung ứng)", text_lower):
        return "📦 Ngành **Quản trị Logistics và chuỗi cung ứng số** (Mã: 7340101EL) có điểm chuẩn năm 2025 là 23.50 điểm (Hệ Cử nhân 4 năm)."

    # 5. Intent: Hỏi về các ngành, mã ngành, điểm chuẩn
    if re.search(r"(mã ngành|mã số|điểm chuẩn|bao nhiêu điểm|điểm trúng tuyển|các ngành|những ngành|chuyên ngành|ngành gì)", text_lower):
        return """🎓 **THÔNG TIN NGÀNH HỌC, MÃ NGÀNH & ĐIỂM CHUẨN VKU:**

**💻 KHỐI MÁY TÍNH & CNTT (Kỹ sư 4.5 năm):**
1. Thiết kế vi mạch bán dẫn (7480108IC) - Điểm: 24.00
2. Trí tuệ nhân tạo (7480107) - Điểm: 21.00
3. Công nghệ thông tin (7480201) - Điểm: 20.00
4. An toàn thông tin (7480202) - Điểm: 19.00
5. Kỹ thuật phần mềm ô tô (7480108AS) - Điểm: 18.00
6. Công nghệ Game (7480201GT) - Điểm: 19.00
7. CNTT - Hợp tác DN (7480201DT) - Điểm: 18.50 *(Cử nhân 4 năm)*

**📊 KHỐI KINH TẾ & TRUYỀN THÔNG (Cử nhân 4 năm):**
1. Quản trị Logistics & chuỗi cung ứng số (7340101EL) - Điểm: 23.50
2. Marketing số (7340115) - Điểm: 23.25
3. Quản trị dịch vụ du lịch & lữ hành số (7340101ET) - Điểm: 23.00
4. Công nghệ tài chính - Fintech (7340205) - Điểm: 22.00
5. Thiết kế Mỹ thuật số (7320106DA) - Điểm: 21.00
6. Quản trị dự án CNTT (7340101IM) - Điểm: 20.00"""

# 6. Intent: Hỏi về khối thi, tổ hợp môn (Đã nâng cấp)
    if re.search(r"(tổ hợp|khối thi|thi khối|xét khối|môn thi|khối nào)", text_lower):
        # Nếu câu hỏi có nhắc đến chữ "ngành", các khối C/B, hoặc cụm từ "có được không", "có xét không"
        # -> Bỏ qua Local Model, đẩy xuống cho AI đọc file txt để phân tích và trả lời chi tiết.
        if re.search(r"(ngành|quản trị|marketing|cntt|vi mạch|c00|khối c|b00|khối b|được không|có xét)", text_lower):
            pass # Bỏ qua, để hàm chạy tiếp xuống dòng "return None" ở cuối
        else:
            return """📚 **Các tổ hợp xét tuyển chủ đạo tại VKU:**
- **A00:** Toán, Vật lý, Hóa học
- **A01:** Toán, Vật lý, Tiếng Anh
- **D01:** Toán, Ngữ văn, Tiếng Anh
- **D07:** Toán, Hóa học, Tiếng Anh
*(Các tổ hợp này dùng chung cho hầu hết các ngành nhé!)*"""

    # 6.5 Intent bổ sung: Trả lời chặn luôn nếu hỏi khối C, khối B (tối ưu tốc độ)
    if re.search(r"(c00|c01|c03|c04|khối c|b00|b08|khối b)", text_lower):
        return "❌ Rất tiếc, hiện tại VKU **KHÔNG** xét tuyển các tổ hợp thuộc khối C (Văn, Sử, Địa) hay khối B (Toán, Hóa, Sinh). Trường chỉ tập trung xét 4 tổ hợp chính là: **A00, A01, D01, D07** thôi bạn nhé!"

    # 7. Intent: Quy trình, hồ sơ nhập học
    if re.search(r"(nhập học|hồ sơ|cần những giấy tờ gì|chuẩn bị gì|thủ tục)", text_lower):
        return """📝 **Quy trình & Hồ sơ nhập học VKU:**
- **Quy trình 3 bước:** Xác nhận trực tuyến Bộ GD&ĐT -> Khai báo trên web VKU -> Nộp hồ sơ trực tiếp tại trường.
- **Hồ sơ cần (Bản sao công chứng):** Giấy báo trúng tuyển (bản chính), Học bạ THPT, Bằng TN hoặc Giấy CNTN tạm thời, Giấy khai sinh, CCCD, Sơ yếu lý lịch, Ảnh thẻ và các giấy tờ ưu tiên (nếu có)."""

    # 8. Intent: Câu lạc bộ / Hoạt động
    if re.search(r"(câu lạc bộ|clb|hoạt động|ngoại khóa|đội nhóm)", text_lower):
        return """🌟 **Danh sách các Câu lạc bộ (CLB) siêu đỉnh tại VKU:**
- **Tình nguyện & Kỹ năng:** CLB Hand In Hand, CLB Kỹ năng.
- **Học thuật:** CLB Vi mạch bán dẫn, CLB Truyền thông VM (VM Media), CLB Sách.
- **Năng khiếu & Thể thao:** CLB Âm nhạc, CLB Võ Karate, CLB Game VKU Esport.
*(Tham gia CLB là cách tuyệt vời để kiếm điểm rèn luyện và có thêm nhiều bạn mới đó nha!)*"""

    # 9. Intent: Cơ sở vật chất / Điều hòa / Thư viện
    if re.search(r"(cơ sở vật chất|điều hòa|máy lạnh|nóng không|phòng học|thư viện)", text_lower):
        return """🏫 **Cơ sở vật chất cực xịn tại VKU:**
- **100% phòng học lý thuyết có Điều hòa (Máy lạnh)**, bao mát mẻ!
- Hệ thống phòng Lab, không gian sáng tạo Maker Space, phòng thực hành Vi mạch/AI cực kỳ hiện đại.
- Thư viện thông minh rộng rãi, không gian xanh mát, góc nào cũng sống ảo được."""

    # 10. Intent: Việc làm / Thực tập
    if re.search(r"(việc làm|thực tập|ra trường|thất nghiệp|làm ở đâu|xin việc)", text_lower):
        return """💼 **Cơ hội việc làm & Thực tập:**
- VKU cam kết 100% sinh viên được thực tập tại doanh nghiệp từ năm 3.
- Mạng lưới đối tác: Hơn 200 tập đoàn lớn (FPT Software, Samsung, Hanwha, NiX Education...).
- Tốt nghiệp VKU bạn có thể làm: Lập trình viên, Kỹ sư Vi mạch/AI, Chuyên viên Marketing số, Quản trị Logistics... Ngành nào cũng đang khát nhân lực!"""

    # 11. Intent: Laptop
    if re.search(r"(laptop|máy tính|cấu hình)", text_lower):
        return """💻 **Tư vấn mua Laptop học tại VKU:**
- Rất cần có Laptop từ năm nhất để thực hành.
- **Cấu hình tối thiểu:** CPU Core i5/Ryzen 5, RAM 16GB, SSD 512GB.
- Nếu học ngành Game, AI hoặc Thiết kế Đồ họa thì nên ưu tiên máy có Card màn hình rời (VGA) nhé."""

    # 12. Intent: Ngoại ngữ / Tiếng Anh / Tiếng Hàn
    if re.search(r"(tiếng anh|ngoại ngữ|tiếng hàn|dốt tiếng anh|kém tiếng anh|học bằng tiếng gì)", text_lower):
        return """🇬🇧🇰🇷 **Học Ngoại ngữ tại VKU:**
- **Tiếng Anh:** Là ngoại ngữ chính. Bạn sẽ được học lại từ cơ bản khi vào trường. Tài liệu IT/Kinh tế số đa phần bằng tiếng Anh nên cố gắng nhé.
- **Tiếng Hàn:** Là ngoại ngữ tự chọn. Tuy nhiên, nếu bạn biết Tiếng Hàn, bạn sẽ có lợi thế cực lớn để lấy học bổng từ các tập đoàn Hàn Quốc (Samsung, Hanwha...) và đi trao đổi sinh viên!"""

    # Nếu không trúng Intent nào -> Đẩy cho AI xử lý
    return None


@bot.message_handler(commands=['start'])
def send_welcome(message):
    user_id = message.chat.id
    user_histories[user_id] = []
    bot.reply_to(message, "Chào bạn! Mình là AI Tư vấn Tuyển sinh của VKU. Mình có thể giúp gì cho bạn?")

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    user_id = message.chat.id
    user_question = message.text
    
    if user_id not in user_histories:
        user_histories[user_id] = []

    print("-" * 50)
    print(f"[!] Câu hỏi: {user_question}")

    # ==========================================
    # BƯỚC 1: KIỂM TRA BẰNG MÔ HÌNH CỤC BỘ TRƯỚC
    # ==========================================
    local_answer = local_intent_matcher(user_question)
    
    if local_answer:
        bot.reply_to(message, local_answer, parse_mode="Markdown")
        print("[OK] Trả lời SIÊU TỐC bằng Local Regex Model.")
        
        user_histories[user_id].append({"role": "user", "content": user_question})
        user_histories[user_id].append({"role": "assistant", "content": local_answer})
        return

    # ==========================================
    # BƯỚC 2: NẾU LOCAL KHÔNG BIẾT -> CHUYỂN CHO AI
    # ==========================================
    processing_msg = bot.reply_to(message, "⏳ Chờ mình tra cứu xíu nhé...")

    # Cập nhật Prompt chống ảo giác Đại học Duy Tân
    system_prompt = f"""
    Bạn là AI Tư vấn tuyển sinh của Trường Đại học Công nghệ Thông tin và Truyền thông Việt - Hàn (Tên gọi khác: VKU, Việt Hàn).
    
    LUẬT THÉP BẮT BUỘC:
    1. Trường VKU trực thuộc ĐẠI HỌC ĐÀ NẴNG (ĐHĐN). TUYỆT ĐỐI KHÔNG trực thuộc Đại học Duy Tân. Trụ sở DUY NHẤT ở Đà Nẵng. Không ở Huế.
    2. CHỈ TRẢ LỜI DỰA TRÊN TEXT DƯỚI ĐÂY. Nếu thông tin không có trong text, hãy trả lời: "Dữ liệu hiện tại của mình chưa có thông tin này, bạn liên hệ hotline 0236.6.552.688 nhé." TUYỆT ĐỐI KHÔNG bịa thêm kiến thức ngoài.
    
    DỮ LIỆU CHÍNH THỨC:
    {vku_data}
    """

    messages_to_send = [{"role": "system", "content": system_prompt}]
    
    for h in user_histories[user_id][-8:]: 
        messages_to_send.append(h)
    
    messages_to_send.append({"role": "user", "content": user_question})

    try:
        start_time = time.time()
        response = g4f.ChatCompletion.create(
            model=g4f.models.gpt_4,
            messages=messages_to_send,
        )
        
        user_histories[user_id].append({"role": "user", "content": user_question})
        user_histories[user_id].append({"role": "assistant", "content": response})

        bot.delete_message(chat_id=message.chat.id, message_id=processing_msg.message_id)
        bot.send_message(message.chat.id, response)
        print(f"[OK] Trả lời bằng AI g4f sau {time.time()-start_time:.2f}s")
        
    except Exception as e:
        bot.edit_message_text(chat_id=message.chat.id, message_id=processing_msg.message_id, text="Hệ thống đang bận, bạn hỏi lại nhé!")
        print(f"[LỖI]: {e}")

bot.infinity_polling(timeout=60)