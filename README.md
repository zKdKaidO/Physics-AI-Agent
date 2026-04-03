# ⚛️ Physics AI Agent: Intelligent Teaching Assistant

[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.x-FF4B4B.svg)](https://streamlit.io/)
[![Google Gemini API](https://img.shields.io/badge/LLM-Google%20Gemini%202.5-orange.svg)](https://ai.google.dev/)

**Physics AI Agent** là một hệ thống Trợ lý Giảng dạy thông minh được thiết kế đặc biệt cho bộ môn Vật Lý. Ứng dụng kiến trúc Đa phương thức gốc (Native Multimodal) từ Google Gemini API, hệ thống có khả năng đọc hiểu trực tiếp các tài liệu học thuật phức tạp (Slide bài giảng, Đề thi PDF chứa công thức, biểu đồ) và hỗ trợ giáo viên tự động hóa quá trình soạn thảo nội dung, giải đáp bài tập.

## 🚀 Live Demo
Trải nghiệm trực tiếp hệ thống đã được triển khai trên Streamlit Community Cloud:
👉 **[Truy cập Physics AI Agent tại đây](https://nnam-physics-ai-agent.streamlit.app/)**

---

## 🎯 Chức năng Cốt lõi (Core Features)

- **Intelligent Document Processing (IDP):** Nhận diện và trích xuất ngữ cảnh trực tiếp từ file PDF mà không làm vỡ định dạng công thức Vật Lý.
- **Tự động Tóm tắt & Trích xuất:** Tự động tổng hợp các định lý cốt lõi và liệt kê công thức kèm theo đơn vị đo chuẩn (SI).
- **Trợ giảng Giải bài tập:** Cung cấp lời giải Step-by-step cho các câu hỏi chưa có đáp án và giải thích sâu về bản chất Vật lý cho các bài đã có lời giải tắt.
- **Stateful Conversation (Trí nhớ Phiên):** Duy trì bộ nhớ ngữ cảnh (Session State) cho phép người dùng liên tục đặt câu hỏi đào sâu về tài liệu đã tải lên như một cuộc hội thoại đa lượt (Multi-turn Chat).
- **Toán học Chuẩn hóa:** Render hoàn hảo các công thức Toán học/Vật lý dưới định dạng chuẩn $\LaTeX$.

---

## ⚙️ Kiến trúc Hệ thống & Luồng xử lý (Pipeline)

Dự án được thiết kế theo kiến trúc **Stateful Agent** trên nền tảng Web, loại bỏ sự phức tạp của Vector Database (như trong các hệ thống RAG truyền thống) bằng cách tận dụng tối đa Cửa sổ Ngữ cảnh (Context Window) lớn của LLM.

**Luồng dữ liệu (Data Pipeline):**
1. **Data Ingestion (Nạp dữ liệu):** Người dùng tải lên file PDF qua giao diện UI. File được lưu tạm trữ (Temporary File System) để đảm bảo an toàn bộ nhớ.
2. **Multimodal Reasoning (Suy luận Đa phương thức):** - Hệ thống khởi tạo đối tượng `ChatSession` thông qua Google GenAI SDK.
   - File PDF và System Prompt (được thiết kế bằng kỹ thuật Prompt Engineering chặt chẽ) được đẩy vào mô hình `gemini-2.5-flash` để khởi tạo bối cảnh (Context).
3. **State Management (Quản lý trạng thái):** Trạng thái hội thoại (`chat_session`) và lịch sử tin nhắn (`messages`) được gắn chặt vào `st.session_state` của Streamlit, đảm bảo Agent không bị mất trí nhớ khi giao diện tải lại.
4. **Execution & Rendering (Thực thi & Hiển thị):**
   - Agent trả về nội dung dưới dạng cấu trúc Markdown kết hợp LaTeX.
   - Streamlit Parser biên dịch kết quả và hiển thị trực quan lên màn hình.
   - File tạm thời (Temp File) được tự động dọn dẹp (Clean up) để giải phóng tài nguyên.

---

## 🛠️ Hướng dẫn Cài đặt Cục bộ (Local Setup)

Dành cho các nhà phát triển muốn clone và phát triển thêm tính năng cho Agent.

**Bước 1: Clone Repository**
```bash
git clone [https://github.com/zKdKaidO/physics-ai-agent.git](https://github.com/zKdKaidO/physics-ai-agent.git)
cd physics-ai-agent