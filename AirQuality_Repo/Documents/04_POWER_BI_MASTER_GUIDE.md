# HƯỚNG DẪN BÁO CÁO POWER BI TOÀN TẬP (MASTER GUIDE)

Tài liệu này hướng dẫn xây dựng Dashboard hoàn chỉnh gồm 2 trang: Tổng quan và Phân tích Chuyên sâu.

---

## PHẦN 1: KẾT NỐI DỮ LIỆU
1.  **Get Data:** Chọn SQL Server -> Database `AirQuality_DW`.
2.  **Select Tables:** Chọn tất cả các bảng Fact và Dim (`FactHourly...`, `FactAnnual...`, `FactPolicy...`, `DimDate`, `DimLocation`, `DimCity`...).
3.  **Model View:** Kiểm tra Relationship.
    *   Đảm bảo `FactPolicyEvent` nối với `DimDate` (qua DateKey) và `DimPolicy`.
    *   Đảm bảo `FactAnnualSummary` nối với `DimCity`.

---

## PHẦN 2: TRANG 1 - TỔNG QUAN CHẤT LƯỢNG KHÔNG KHÍ
*Mục tiêu: Theo dõi chỉ số hiện tại và xu hướng cơ bản.*

### 1. Các chỉ số chính (KPI Cards)
*   Tạo Measure: `Avg AQI = AVERAGE(FactHourlyMeasurement[AQI])`.
*   Sử dụng **Multi-row Card** để hiển thị AQI và PM2.5 cho Hà Nội và Bắc Kinh.

### 2. Biểu đồ xu hướng (Line Chart)
*   **Trục X:** `Year` (DimDate).
*   **Trục Y:** `Avg AQI`.
*   **Legend:** `City` (DimLocation).

### 3. Biểu đồ nhiệt (Matrix/Heatmap)
*   Thể hiện mức độ ô nhiễm theo Giờ trong ngày và Ngày trong tuần.

---

## PHẦN 3: TRANG 2 - PHÂN TÍCH HIỆU QUẢ CHÍNH SÁCH (NÂNG CAO)
*Mục tiêu: Chứng minh tác động của chính sách lên môi trường.*

### 1. Bộ lọc (Slicer)
*   Sử dụng `CityName` từ `DimCity`. Chọn "Beijing".

### 2. Biểu đồ Xu hướng 10 năm (Line Chart)
*   **Dữ liệu:** Dùng bảng `FactAnnualSummary`.
*   **Trục X:** `Year`.
*   **Trục Y:** `Avg_PM25`.
*   **Legend:** `CityName`.
*   *Ý nghĩa:* Thấy rõ đường biểu diễn đi xuống dốc (giảm ô nhiễm).

### 3. Bảng Sự kiện (Table)
*   **Dữ liệu:** Kết hợp `DimDate`, `DimPolicy`, `FactPolicyEvent`.
*   **Cột:** `FullDate`, `PolicyName`, `ImpactLevel`.
*   *Ý nghĩa:* Đối chiếu các mốc giảm của biểu đồ trên với các sự kiện trong bảng này.

### 4. Biểu đồ So sánh AQI (Clustered Column Chart)
*   **Dữ liệu:** `FactAnnualSummary`.
*   **Trục X:** `Year`.
*   **Trục Y:** `Avg_AQI`.
*   **Legend:** `CityName`.
*   **Định dạng:** Tô màu Xanh cho Bắc Kinh (Cải thiện) và Đỏ cho Hà Nội (Cảnh báo).

---

## PHẦN 4: XUẤT BÁO CÁO
1.  Thêm Tiêu đề lớn cho mỗi trang.
2.  Chỉnh Theme màu sắc cho đồng bộ.
3.  **Export to PDF** để nộp đồ án.
