import streamlit as st
import os
import tempfile
from dotenv import load_dotenv
from module_extractor import PhysicsContentExtractor 

st.set_page_config(page_title="AI Physics Agent", page_icon="⚛️", layout="wide")
st.title("⚛️ AI Agent: Trợ lý Giảng dạy Vật Lý")

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    st.error("⚠️ LỖI: Chưa có API Key.")
    st.stop()

# ================= QUẢN LÝ BỘ NHỚ (STATE) =================
# Khởi tạo các biến nhớ để không bị mất khi web reload
if "chat_session" not in st.session_state:
    st.session_state.chat_session = None
if "messages" not in st.session_state:
    st.session_state.messages = []

# ================= SIDEBAR: KHU VỰC TẢI TÀI LIỆU =================
with st.sidebar:
    st.header("1. Nạp Tài Liệu")
    uploaded_file = st.file_uploader("Tải Slide/Đề thi (PDF)", type=["pdf"])
    
    if uploaded_file and st.button("Bắt đầu phiên học", type="primary"):
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
            tmp_file.write(uploaded_file.getvalue())
            tmp_path = tmp_file.name

        with st.spinner("Agent đang đọc tài liệu..."):
            try:
                # Gọi hàm mới để lấy đối tượng chat
                extractor = PhysicsContentExtractor(api_key=api_key)
                chat_obj, first_reply = extractor.create_chat_session(tmp_path)
                
                # LƯU VÀO BỘ NHỚ RAM CỦA WEB
                st.session_state.chat_session = chat_obj
                st.session_state.messages = [{"role": "assistant", "content": first_reply}]
                
                st.success("✅ Đã kết nối trí nhớ thành công!")
            except Exception as e:
                st.error(f"❌ Lỗi: {e}")
            finally:
                if os.path.exists(tmp_path):
                    os.remove(tmp_path)

# ================= KHU VỰC CHAT CHÍNH =================
# 1. Vẽ lại toàn bộ lịch sử chat cũ
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# 2. Ô nhập liệu cho câu hỏi mới
if st.session_state.chat_session is not None:
    user_query = st.chat_input("VD: Giải thích lại bản chất của gia tốc trong bài 2...")
    
    if user_query:
        # Hiển thị câu hỏi của người dùng
        st.session_state.messages.append({"role": "user", "content": user_query})
        with st.chat_message("user"):
            st.markdown(user_query)
        
        # Gửi câu hỏi vào Agent và chờ phản hồi
        with st.chat_message("assistant"):
            with st.spinner("Đang suy luận..."):
                response = st.session_state.chat_session.send_message(user_query)
                st.markdown(response.text)
                # Lưu câu trả lời vào bộ nhớ
                st.session_state.messages.append({"role": "assistant", "content": response.text})
else:
    st.info("👈 Vui lòng tải tài liệu ở cột bên trái để bắt đầu trò chuyện.")