import streamlit as st
import os
import tempfile
from dotenv import load_dotenv
# Import Class lõi mà bạn đã dọn dẹp và chạy thành công
from module_extractor import PhysicsContentExtractor 

# 1. Cấu hình giao diện Web
st.set_page_config(page_title="AI Physics Agent", page_icon="⚛️", layout="wide")
st.title("⚛️ AI Agent: Trợ lý Giảng dạy Vật Lý")
st.markdown("""
Hệ thống xử lý tài liệu đa phương thức. Hãy tải lên Slide bài giảng hoặc Đề thi Vật lý (định dạng PDF). 
Agent sẽ tự động tóm tắt lý thuyết, liệt kê công thức và giải chi tiết các câu hỏi.
""")

# 2. Tải API Key
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    st.error("⚠️ Hệ thống chưa được kết nối! Vui lòng kiểm tra file .env")
    st.stop() # Dừng vẽ UI nếu không có Key

# 3. Khu vực Upload File
uploaded_file = st.file_uploader("Kéo thả file PDF vào đây", type=["pdf"])

# 4. Xử lý Logic khi người dùng bấm nút
if uploaded_file is not None:
    if st.button("🚀 Bắt đầu trích xuất nội dung", type="primary"):
        
        # Streamlit lưu file trên RAM (bytes). Class của chúng ta cần đường dẫn vật lý (path).
        # Do đó, ta phải lưu tạm file này xuống ổ cứng.
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
            tmp_file.write(uploaded_file.getvalue())
            tmp_path = tmp_file.name

        # Hiển thị vòng xoay chờ đợi
        with st.spinner("Agent đang đọc tài liệu và suy luận... (10-30s)"):
            try:
                # Khởi tạo bộ não AI và truyền file vào
                extractor = PhysicsContentExtractor(api_key=api_key)
                result = extractor.extract(tmp_path)
                
                if result:
                    st.success("✅ Trích xuất thành công!")
                    # Hiển thị kết quả dưới dạng Markdown đẹp mắt
                    st.markdown("---")
                    st.markdown(result)
                else:
                    st.warning("⚠️ Agent không thể trả về kết quả.")
                    
            except Exception as e:
                st.error(f"❌ Có lỗi hệ thống: {e}")
                
            finally:
                # Dọn dẹp rác: Xóa file tạm trên máy tính sau khi xử lý xong
                if os.path.exists(tmp_path):
                    os.remove(tmp_path)