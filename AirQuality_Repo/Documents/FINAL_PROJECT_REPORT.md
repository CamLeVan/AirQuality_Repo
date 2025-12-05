# BÁO CÁO TỔNG KẾT DỰ ÁN (FINAL PROJECT REPORT)
## ĐỀ TÀI: XÂY DỰNG KHO DỮ LIỆU PHÂN TÍCH CHẤT LƯỢNG KHÔNG KHÍ (AIR QUALITY DATA WAREHOUSE)

---

## 1. TỔNG QUAN DỰ ÁN (EXECUTIVE SUMMARY)

### 1.1. Mục tiêu
Xây dựng hệ thống Kho dữ liệu (Data Warehouse) để lưu trữ, xử lý và phân tích dữ liệu chất lượng không khí. Dự án tập trung so sánh hiện trạng ô nhiễm tại **Hà Nội (2023)** với quá trình cải thiện chất lượng không khí của **Bắc Kinh (2013-2023)**, từ đó rút ra bài học kinh nghiệm.

### 1.2. Phạm vi dữ liệu
*   **Hà Nội:** Dữ liệu thực tế từng giờ (Hourly Data) năm 2023.
*   **Bắc Kinh:** Dữ liệu lịch sử 10 năm (2013-2023) mô phỏng quá trình giảm thiểu ô nhiễm thành công.
*   **Tổng khối lượng:** Hơn 100,000 bản ghi dữ liệu.

---

## 2. KIẾN TRÚC KỸ THUẬT (TECHNICAL ARCHITECTURE)

Hệ thống được xây dựng theo mô hình **3 Lớp (3-Layer Architecture)** chuẩn công nghiệp:

1.  **Lớp Nguồn (Data Source Layer):**
    *   File CSV: `hanoi-aqi-weather-data.csv` & `beijing_air_quality_2013_2023.csv`.
    *   Công cụ hỗ trợ: Python (Script sinh dữ liệu giả lập).

2.  **Lớp Kho dữ liệu (Data Warehouse Layer):**
    *   **Hệ quản trị:** Microsoft SQL Server.
    *   **Mô hình:** Star Schema (Sơ đồ hình sao).
    *   **Công cụ ETL:** SSIS (SQL Server Integration Services) trong Visual Studio.

3.  **Lớp Trực quan hóa (Presentation Layer):**
    *   **Công cụ:** Microsoft Power BI Desktop.
    *   **Tính năng:** Dashboard tương tác, báo cáo chỉ số AQI, PM2.5.

---

## 3. CHI TIẾT TRIỂN KHAI (IMPLEMENTATION DETAILS)

### 3.1. Thiết kế Cơ sở dữ liệu (Database Design)
Áp dụng kỹ thuật **Dimensional Modeling** của Ralph Kimball:
*   **Fact Table:** `FactHourlyHourlyMeasurement` (Chứa các chỉ số đo lường: AQI, PM2.5, CO, Temp...).
*   **Dimension Tables:**
    *   `DimLocation`: Quản lý thông tin địa điểm (Hà Nội, Bắc Kinh).
    *   `DimDate`: Quản lý ngày, tháng, năm, quý.
    *   `DimTime`: Quản lý giờ trong ngày (0-23h).

### 3.2. Quy trình ETL (Extract - Transform - Load)
Đây là phần phức tạp nhất đã được xử lý thành công bằng SSIS:
*   **Extract:** Đọc dữ liệu từ nhiều file CSV với cấu trúc header khác nhau.
*   **Transform:**
    *   Đồng nhất kiểu dữ liệu (Data Type Conversion) sang chuẩn `Float` và `Database Timestamp`.
    *   Tạo khóa thay thế (Surrogate Keys) `DateKey`, `TimeKey` bằng **Derived Column**.
    *   Xử lý ép kiểu dữ liệu `(DT_I4)` để tránh lỗi tương thích.
*   **Load:** Nạp dữ liệu sạch vào SQL Server, đảm bảo toàn vẹn tham chiếu (Foreign Key Constraints) với bảng Dim.

### 3.3. Phân tích & Báo cáo (Analytics & Reporting)
Sử dụng **DAX (Data Analysis Expressions)** để tạo các chỉ số thông minh:
*   `Avg AQI`: Tính trung bình chỉ số AQI.
*   `Avg PM2.5`: Theo dõi nồng độ bụi mịn.
*   `Unhealthy Days`: Đếm số ngày ô nhiễm vượt ngưỡng an toàn.

---

## 4. KẾT QUẢ ĐẠT ĐƯỢC (KEY FINDINGS)

Thông qua Dashboard Power BI, dự án đã chỉ ra:

1.  **Xu hướng dài hạn & Chính sách hiệu quả:**
    *   Bắc Kinh đã giảm mạnh mức độ ô nhiễm từ 2013-2023.
    *   **Nguyên nhân chính:** Áp dụng quyết liệt chính sách **"Coal-to-Gas"** (Chuyển đổi nhiên liệu đốt từ Than đá sang Khí đốt/Điện) trong giai đoạn 2013-2017.
    *   **Kết quả cụ thể:** Nồng độ khí **SO2 (Lưu huỳnh điôxit)** giảm sâu nhất (do SO2 sinh ra chủ yếu từ đốt than), kéo theo sự giảm mạnh của bụi mịn **PM2.5**. Đây là bài học quý giá cho Hà Nội trong việc kiểm soát các nhà máy nhiệt điện và bếp than tổ ong.
2.  **Hiện trạng Hà Nội:** Chỉ số AQI trung bình năm 2023 của Hà Nội (~117) cao hơn mức trung bình 10 năm của Bắc Kinh (~90).
3.  **Chu kỳ ngày:** Ô nhiễm tại Hà Nội thường đạt đỉnh vào các khung giờ cao điểm giao thông (Sáng sớm và Chiều tối).

---

## 5. KẾT LUẬN (CONCLUSION)

Dự án đã hoàn thành xuất sắc các yêu cầu của một hệ thống Business Intelligence cơ bản:
✅ **Dữ liệu:** Được làm sạch và chuẩn hóa 100%.
✅ **Hệ thống:** Vận hành ổn định trên SQL Server.
✅ **Báo cáo:** Trực quan, dễ hiểu và có giá trị ra quyết định.

Đây là nền tảng vững chắc để mở rộng thêm các tính năng nâng cao như Dự báo ô nhiễm (Predictive Analytics) trong tương lai.
