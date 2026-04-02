import os
import argparse
import time
from dotenv import load_dotenv
from google import genai
from google.genai import types

class PhysicsContentExtractor:
    def __init__(self, api_key: str):
        """Khởi tạo Client với SDK mới nhất của Google."""
        self.client = genai.Client(api_key=api_key)
        # Nâng cấp lên model thế hệ mới nhất cho tác vụ phức tạp
        self.model_id = 'gemini-2.5-flash' 

    def _upload_and_wait(self, file_path: str):
        """Upload file bằng hệ thống File API mới."""
        print(f"[*] Đang tải lên tài liệu: {file_path}...")
        uploaded_file = self.client.files.upload(file=file_path)
        
        # Kiểm tra trạng thái xử lý
        while uploaded_file.state.name == "PROCESSING":
            print("[*] Đang xử lý tài liệu trên cloud...", end="\r")
            time.sleep(2)
            uploaded_file = self.client.files.get(name=uploaded_file.name)
            
        if uploaded_file.state.name == "FAILED":
            raise ValueError("Lỗi: Hệ thống không thể xử lý file PDF này.")
            
        print("\n[*] Tải lên và xử lý hoàn tất!")
        return uploaded_file

    def extract(self, pdf_path: str):
        """Hàm chính: Sinh nội dung từ tài liệu đa phương thức."""
        if not os.path.exists(pdf_path):
            print(f"[!] Không tìm thấy file: {pdf_path}")
            return None

        uploaded_file = None
        try:
            uploaded_file = self._upload_and_wait(pdf_path)
            
            system_prompt = """
            Bạn là một trợ lý học thuật chuyên nghiệp môn Vật Lý, có kiến thức sâu rộng và khả năng giảng giải đa chiều.
            Nhiệm vụ:
            1. PHẦN KIẾN THỨC:
            - Dựa vào tài liệu PDF bài giảng được cung cấp, hãy tóm tắt đầy đủ nội dung lý thuyết.
            - Giải thích chi tiết tất cả công thức, định lý, định luật vật lý xuất hiện trong bài.
            - Mở rộng thêm kiến thức liên quan từ nhiều góc độ (lịch sử phát triển, ứng dụng thực tiễn, liên hệ với các ngành khác, ví dụ minh họa).
            - Trình bày theo cách giúp học sinh thấy được chiều sâu và sự phong phú của vật lý.

            2. PHẦN BÀI TẬP/CÂU HỎI:
            - Quét toàn bộ câu hỏi trong slide (không cần ghi lại nguyên văn).
            - Với câu chưa có đáp án: giải chi tiết, dễ hiểu, kèm ví dụ minh họa thực tế.
            - Với câu đã có đáp án/lời giải tắt: kiểm tra tính hợp lý, sau đó giải thích lại rõ ràng hơn, thêm ví dụ để làm sáng tỏ bản chất vật lý.

            3. YÊU CẦU TRÌNH BÀY (QUAN TRỌNG):
            - Định dạng kết quả bằng Markdown chuyên nghiệp.
            - Trình bày toàn bộ kết quả bằng Markdown.
            - TUYỆT ĐỐI không dùng `\[ ... \]` hay `\( ... \)` cho công thức toán học/vật lý.
            - Với công thức nằm lẫn trong văn bản, BẮT BUỘC bọc trong một dấu đô-la: $cong_thuc$. Ví dụ: Vận tốc $v = 10 m/s$.
            - Với công thức đứng độc lập trên một dòng, BẮT BUỘC bọc trong hai dấu đô-la: $$cong_thuc$$.
            - Có cấu trúc rõ ràng: tiêu đề, mục lục, phân chia phần kiến thức và phần bài tập.
            - Văn phong: học thuật, dễ hiểu, giàu ví dụ, thể hiện sự am hiểu sâu rộng.

            Mục tiêu: Tạo ra một tài liệu vừa là bản tóm tắt lý thuyết, vừa là lời giải chi tiết cho bài tập, giúp học sinh hiểu sâu và hứng thú với môn Vật Lý.

            """
            
            print("[*] Đang suy luận và biên soạn nội dung... (Có thể mất 10-30s)")
            
            # Cấu trúc gọi API mới
            response = self.client.models.generate_content(
                model=self.model_id,
                contents=[uploaded_file, system_prompt]
            )
            return response.text
            
        except Exception as e:
            print(f"[!] Đã xảy ra lỗi trong quá trình xử lý: {e}")
            return None
            
        finally:
            # Xóa file an toàn
            if uploaded_file:
                try:
                    self.client.files.delete(name=uploaded_file.name)
                    print(f"[*] Đã dọn dẹp file tạm trên cloud.")
                except Exception as cleanup_error:
                    print(f"[!] Không thể xóa file tạm: {cleanup_error}")

# ================= CÁCH SỬ DỤNG VỚI CLI =================
if __name__ == "__main__":
    load_dotenv() 
    MY_API_KEY = os.getenv("GEMINI_API_KEY") 
    
    if not MY_API_KEY:
        print("[!] LỖI: Chưa tìm thấy API Key. Hãy kiểm tra lại file .env")
        exit()

    parser = argparse.ArgumentParser(description="AI Agent: Trích xuất & Tóm tắt Slide Vật Lý")
    parser.add_argument(
        "--file", 
        type=str, 
        required=True, 
        help="Đường dẫn tĩnh hoặc tương đối đến file PDF của bạn"
    )
    args = parser.parse_args()

    pdf_path = args.file
    print(f"\n[*] Bắt đầu quy trình xử lý cho file: {pdf_path}")
    
    extractor = PhysicsContentExtractor(api_key=MY_API_KEY)
    result = extractor.extract(pdf_path)
    
    if result:
        print("\n" + "="*60)
        print(" KẾT QUẢ TRÍCH XUẤT TỪ AI AGENT")
        print("="*60 + "\n")
        print(result)