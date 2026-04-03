import streamlit as st
import os
import tempfile
from dotenv import load_dotenv
from module_extractor import PhysicsContentExtractor 

# 1. Cấu hình trang phải nằm trên cùng
st.set_page_config(page_title="Physics Notebook", page_icon="📓", layout="wide")

# 2. CSS Tiêm ngầm (Custom CSS Injection) để giống NotebookLM
custom_css = """
<style>
    /* Ẩn menu mặc định của Streamlit */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Căn chỉnh lại khoảng không gian chính */
    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
        max-width: 65rem;
    }
    
    /* Làm đẹp Sidebar (Cột Nguồn dữ liệu) */
    [data-testid="stSidebar"] {
        background-color: #1e1e1e;
        border-right: 1px solid #3c4043;
    }
    
    /* Tùy chỉnh bong bóng chat */
    .stChatMessage {
        background-color: transparent;
        border-radius: 10px;
        padding: 10px;
        margin-bottom: 10px;
    }
    [data-testid="chatAvatarIcon-user"] {
        background-color: #3c4043;
    }
    [data-testid="chatAvatarIcon-assistant"] {
        background-color: #8ab4f8;
    }
    
    /* Làm đẹp nút gợi ý */
    .stButton>button {
        border-radius: 20px;
        border: 1px solid #5f6368;
        background-color: #131314;
        color: #e8eaed;
        transition: all 0.3s;
    }
    .stButton>button:hover {
        border-color: #8ab4f8;
        color: #8ab4f8;
    }
</style>
"""
st.markdown(custom_css, unsafe_allow_html=True)

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

if "extractor" not in st.session_state:
    # Giữ cổng kết nối sống sót vĩnh viễn
    st.session_state.extractor = PhysicsContentExtractor(api_key=api_key)
if "chat_session" not in st.session_state:
    st.session_state.chat_session = None
if "messages" not in st.session_state:
    st.session_state.messages = []

# ================= SIDEBAR: NGUỒN DỮ LIỆU (Giống cột trái NotebookLM) =================
with st.sidebar:
    st.title("📓 Nguồn dữ liệu")
    st.markdown("---")
    
    uploaded_file = st.file_uploader("Thêm nguồn (PDF)", type=["pdf"], label_visibility="collapsed")
    
    if uploaded_file:
        st.info(f"📄 {uploaded_file.name}")
        if st.button("Tạo bản tóm tắt & Khởi tạo Chat", type="primary", use_container_width=True):
            with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
                tmp_file.write(uploaded_file.getvalue())
                tmp_path = tmp_file.name

            with st.spinner("Đang đọc nguồn dữ liệu..."):
                try:
                    # SỬ DỤNG EXTRACTOR TỪ SESSION_STATE, KHÔNG TẠO MỚI
                    chat_obj, first_reply = st.session_state.extractor.create_chat_session(tmp_path)
                    
                    st.session_state.chat_session = chat_obj
                    st.session_state.messages = [{"role": "assistant", "content": first_reply}]
                    st.success("Sẵn sàng!")
                except Exception as e:
                    st.error(f"Lỗi: {e}")
                finally:
                    if os.path.exists(tmp_path):
                        os.remove(tmp_path)

# ================= MAIN AREA: HỘI THOẠI (Giống không gian giữa NotebookLM) =================
st.title("⚛️ Physics Teaching Assistant") # Bạn có thể đổi thành tên bài học
st.caption("Dựa trên nguồn dữ liệu bạn cung cấp, hãy đặt câu hỏi để khám phá nội dung.")

# Hiển thị lịch sử chat
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Nút gợi ý (Suggested Questions)
if st.session_state.chat_session is not None:
    st.markdown("<br>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns(3)
    
    # Bắt sự kiện khi click vào nút gợi ý
    suggestion = None
    with col1:
        if st.button("Tóm tắt lại các công thức chính"): suggestion = "Tóm tắt lại các công thức chính"
    with col2:
        if st.button("Giải thích lại các bài tập khó"): suggestion = "Giải thích lại các bài tập khó"
    with col3:
        if st.button("Đưa ra một ví dụ thực tế"): suggestion = "Đưa ra một ví dụ thực tế"

    # Ô chat chính
    user_query = st.chat_input("Bắt đầu nhập...")
    
    # Nếu người dùng gõ hoặc bấm nút gợi ý
    active_query = user_query or suggestion
    
    if active_query:
        st.session_state.messages.append({"role": "user", "content": active_query})
        with st.chat_message("user"):
            st.markdown(active_query)
        
        with st.chat_message("assistant"):
            with st.spinner("Đang phân tích..."):
                response = st.session_state.chat_session.send_message(active_query)
                st.markdown(response.text)
                st.session_state.messages.append({"role": "assistant", "content": response.text})
                st.rerun() # Refresh lại trang để reset các nút gợi ý
else:
    st.info("👈 Vui lòng thêm nguồn dữ liệu ở cột bên trái để bắt đầu trò chuyện.")