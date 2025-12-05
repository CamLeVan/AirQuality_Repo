# DANH SÁCH HÌNH ẢNH CẦN CHỤP CHO BÁO CÁO

Để hoàn thiện báo cáo, bạn cần chụp các hình ảnh sau và chèn vào các vị trí `[CHÈN HÌNH ẢNH X]` trong file Word.

---

## 1. SQL Server (Database)
*   **[HÌNH ẢNH 1] Sơ đồ Star Schema:**
    *   Mở SSMS -> Database Diagrams -> Tạo diagram mới -> Kéo hết các bảng vào.
    *   Chụp ảnh sơ đồ quan hệ giữa Fact và Dim.

## 2. SSIS (Visual Studio)
*   **[HÌNH ẢNH 2] Control Flow:**
    *   Chụp màn hình tab Control Flow, thấy rõ 3 hộp: `DFT_Load_AirQuality`, `DFT_Load_AnnualSummary`, `DFT_Load_PolicyEvents` nối với nhau.
*   **[HÌNH ẢNH 3] Data Flow - Hourly:**
    *   Double-click vào `DFT_Load_AirQuality`. Chụp ảnh luồng dữ liệu (Source -> Derived Column -> Dest).
*   **[HÌNH ẢNH 4] Data Flow - Annual:**
    *   Double-click vào `DFT_Load_AnnualSummary`. Chụp ảnh luồng có hộp **Aggregate**.
*   **[HÌNH ẢNH 5] Data Flow - Policy:**
    *   Double-click vào `DFT_Load_PolicyEvents`. Chụp ảnh luồng có hộp **Lookup**.

## 3. Power BI
*   **[HÌNH ẢNH 6] Model View:**
    *   Vào tab Model View (icon sơ đồ cây). Chụp ảnh các bảng nối dây với nhau.
*   **[HÌNH ẢNH 7] Dashboard Overview:**
    *   Chụp trang báo cáo 1 (Tổng quan).
*   **[HÌNH ẢNH 8] Dashboard Policy Analysis:**
    *   Chụp trang báo cáo 2 (Phân tích Chính sách) - Trang mà có biểu đồ cột xanh/đỏ so sánh Bắc Kinh và Hà Nội.

---
**Lưu ý:** Khi chụp ảnh, cố gắng để giao diện sáng sủa, rõ nét các con số và tên bảng.
