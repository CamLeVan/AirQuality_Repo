TRƯỜNG ĐẠI HỌC CÔNG NGHỆ THÔNG TIN VÀ
TRUYỀN THÔNG VIỆT – HÀN
KHOA KHOA HỌC MÁY TÍNH

# BÁO CÁO KHO DỮ LIỆU

## ĐỀ TÀI: XÂY DỰNG KHO DỮ LIỆU CHO GIÁM SÁT CHẤT LƯỢNG KHÔNG KHÍ ĐÔ THỊ (HÀ NỘI & BẮC KINH)

**Sinh viên thực hiện:**
1.  Lê Văn Cảm - 23IT.B016
2.  Phạm Mai Gia Huy - 23IT.B081
3.  Hoàng Văn Quyến - 23IT.B182

**Giảng viên hướng dẫn:** ThS. Mai Lam

**Đà Nẵng, tháng 12 năm 2025**

---

## LỜI MỞ ĐẦU

Trong những năm gần đây, vấn đề ô nhiễm không khí đã trở thành mối quan tâm hàng đầu của nhiều quốc gia. Chất lượng không khí không chỉ ảnh hưởng trực tiếp đến sức khỏe cộng đồng mà còn tác động lâu dài đến môi trường và kinh tế.

Báo cáo này trình bày quy trình xây dựng hệ thống kho dữ liệu (Data Warehouse) phục vụ công tác giám sát chất lượng không khí, so sánh giữa **Hà Nội (2023)** và **Bắc Kinh (2013-2023)**. Nội dung bao gồm: thiết kế mô hình Star Schema, triển khai quy trình ETL toàn diện bằng SSIS cho cả 3 bảng Fact, và trực quan hóa dữ liệu bằng Power BI nhằm cung cấp góc nhìn trực quan hỗ trợ ra quyết định.

---

## LỜI CẢM ƠN

Trước tiên, chúng em xin bày tỏ lòng biết ơn sâu sắc tới các thầy cô giáo trong khoa Khoa học Máy tính, đặc biệt là **Thầy Mai Lam** đã tận tình hướng dẫn, chỉ bảo và động viên chúng em trong suốt quá trình thực hiện đồ án này.

---

## MỤC LỤC
1.  CHƯƠNG 1. GIỚI THIỆU ĐỀ TÀI
2.  CHƯƠNG 2. PHÂN TÍCH VÀ THIẾT KẾ
3.  CHƯƠNG 3. TRIỂN KHAI KHO DỮ LIỆU (ETL VỚI SSIS)
4.  CHƯƠNG 4. PHÂN TÍCH VÀ TRỰC QUAN HÓA (POWER BI)
5.  KẾT LUẬN VÀ HƯỚNG PHÁT TRIỂN

---

## CHƯƠNG 1. GIỚI THIỆU ĐỀ TÀI

### 1.1. Tổng quan đề tài
Hiện nay, vấn đề ô nhiễm không khí tại Hà Nội đang ở mức báo động. Nhóm thực hiện đề tài nhằm:
*   Tích hợp dữ liệu đa nguồn (Hà Nội & Bắc Kinh).
*   Chuẩn hóa và lưu trữ dữ liệu lịch sử.
*   Xây dựng báo cáo so sánh trực quan.

### 1.2. Mục tiêu đề tài
*   Thiết kế mô hình Star Schema cho dữ liệu không khí.
*   Thực hiện ETL trích xuất dữ liệu từ CSV, làm sạch và nạp vào SQL Server.
*   Phân tích xu hướng ô nhiễm theo thời gian và so sánh hiệu quả chính sách môi trường.

---

## CHƯƠNG 2: PHÂN TÍCH VÀ THIẾT KẾ

### 2.1. Phân tích Dữ liệu Nguồn
*   **Nguồn 1:** `hanoi-aqi-weather-data.csv` (Dữ liệu thực tế 2023).
*   **Nguồn 2:** `beijing_air_quality_2013_2023.csv` (Dữ liệu lịch sử 10 năm).
*   **Nguồn 3:** `policy_events.csv` (Dữ liệu sự kiện chính sách môi trường).

### 2.2. Thiết Kế Mô Hình Star Schema
Mô hình được thiết kế mở rộng với **3 Bảng Fact** để phục vụ các nhu cầu phân tích khác nhau:

**[CHÈN HÌNH ẢNH 1: Sơ đồ Star Schema trong SQL Server (Database Diagram)]**

**1. Fact Table Chính: `FactHourlyMeasurement`**
*   Lưu trữ dữ liệu đo đạc chi tiết từng giờ.
*   Dùng để phân tích chi tiết, tìm hiểu nguyên nhân gốc rễ.

**2. Fact Table Tổng hợp: `FactAnnualSummary`**
*   Lưu trữ dữ liệu đã được cộng gộp theo năm.
*   Dùng để vẽ biểu đồ xu hướng dài hạn với tốc độ truy vấn cực nhanh.

**3. Fact Table Sự kiện: `FactPolicyEvent`**
*   Lưu trữ các mốc thời gian áp dụng chính sách môi trường.
*   Dùng để đánh giá tác động của chính sách.

---

## CHƯƠNG 3: TRIỂN KHAI KHO DỮ LIỆU (ETL VỚI SSIS)

### 3.1. Quy trình ETL tổng quan
Hệ thống sử dụng công cụ **SQL Server Integration Services (SSIS)** để xây dựng toàn bộ quy trình nạp dữ liệu.

**[CHÈN HÌNH ẢNH 2: Giao diện Control Flow tổng quát trong SSIS]**

### 3.2. Triển khai ETL cho FactHourlyMeasurement (Dữ liệu lớn)
1.  **Extract:** Đọc dữ liệu từ 2 file CSV khác nhau (Hà Nội & Bắc Kinh).
2.  **Transform:**
    *   **Data Conversion:** Chuyển đổi toàn bộ dữ liệu số sang kiểu `float`.
    *   **Derived Column:** Tạo `DateKey`, `TimeKey` và `LocationKey`.
3.  **Load:** Nạp hơn 100,000 dòng vào bảng `FactHourlyMeasurement`.

**[CHÈN HÌNH ẢNH 3: Data Flow Task nạp dữ liệu Hourly (các hộp xanh lá cây)]**

### 3.3. Triển khai ETL Nâng cao cho FactAnnualSummary (Aggregation)
Nhóm sử dụng **SSIS Data Flow** để thực hiện tính toán tổng hợp:
1.  **Source:** Đọc dữ liệu từ `FactHourlyMeasurement`.
2.  **Transform:**
    *   **Sort:** Sắp xếp dữ liệu theo Năm và Thành phố.
    *   **Aggregate:** Tính trung bình (`AVG`) cho AQI, PM2.5 theo từng năm.
3.  **Load:** Nạp kết quả vào bảng `FactAnnualSummary`.

**[CHÈN HÌNH ẢNH 4: Data Flow Task nạp dữ liệu Annual (có hộp Aggregate)]**

### 3.4. Triển khai ETL Nâng cao cho FactPolicyEvent (Lookup)
Quy trình xử lý dữ liệu sự kiện phức tạp với kỹ thuật Lookup:
1.  **Source:** Đọc file `policy_events.csv`.
2.  **Transform:**
    *   **Lookup City:** Tra cứu `CityKey` từ bảng `DimCity`.
    *   **Lookup Policy:** Tra cứu `PolicyKey` từ bảng `DimPolicy`.
    *   **Derived Column:** Biến đổi ngày sự kiện thành `DateKey`.
3.  **Load:** Nạp dữ liệu sạch vào bảng `FactPolicyEvent`.

**[CHÈN HÌNH ẢNH 5: Data Flow Task nạp dữ liệu Policy (có hộp Lookup)]**

---

## CHƯƠNG 4: PHÂN TÍCH VÀ TRỰC QUAN HÓA (POWER BI)

### 4.1. Kết nối và Mô hình hóa
Kết nối Power BI với SQL Server `AirQuality_DW`, thiết lập mối quan hệ hình sao (Star Schema).

**[CHÈN HÌNH ẢNH 6: Model View trong Power BI (Sơ đồ quan hệ)]**

### 4.2. Các chỉ số phân tích (DAX)
Xây dựng các Measure quan trọng: `Avg AQI`, `Avg PM2.5`, `Unhealthy Days`.

### 4.3. Dashboard Tổng quan (Overview)
Trang báo cáo này cung cấp cái nhìn tổng thể về chất lượng không khí hiện tại và xu hướng theo giờ trong ngày.

**[CHÈN HÌNH ẢNH 7: Trang báo cáo Overview (Biểu đồ đường + Thẻ số)]**

### 4.4. Dashboard Phân tích Chính sách (Advanced)
Trang báo cáo chuyên sâu so sánh hiệu quả giảm ô nhiễm giữa Bắc Kinh và Hà Nội trong 10 năm.

**[CHÈN HÌNH ẢNH 8: Trang báo cáo Policy Analysis (Biểu đồ cột so sánh + Bảng sự kiện)]**

### 4.5. Bài học kinh nghiệm và Đề xuất giải pháp
Dựa trên kết quả phân tích dữ liệu, nhóm rút ra các bài học quan trọng:

1.  **Hiệu quả của chính sách "Coal-to-Gas":**
    *   Dữ liệu cho thấy chỉ số PM2.5 tại Bắc Kinh giảm mạnh ngay sau năm 2014 (thời điểm áp dụng chính sách cấm than).
    *   **Đề xuất cho Hà Nội:** Cần đẩy nhanh lộ trình loại bỏ bếp than tổ ong và chuyển đổi các nhà máy nhiệt điện cũ sang sử dụng khí hoặc năng lượng tái tạo.

2.  **Kiểm soát khí thải phương tiện:**
    *   Năm 2017, Bắc Kinh áp dụng chuẩn khí thải mới, biểu đồ tiếp tục cho thấy xu hướng giảm sâu.
    *   **Đề xuất cho Hà Nội:** Áp dụng tiêu chuẩn khí thải Euro 5/6 cho xe cơ giới và hạn chế xe cá nhân vào nội đô giờ cao điểm.

3.  **Hệ thống cảnh báo sớm:**
    *   Dữ liệu cho thấy ô nhiễm thường tăng vọt vào mùa đông.
    *   **Đề xuất:** Xây dựng hệ thống cảnh báo đỏ (Red Alert) dựa trên dữ liệu dự báo để người dân chủ động phòng tránh.

---

## KẾT LUẬN

### 1. Kết quả đạt được
*   Xây dựng thành công Kho dữ liệu hoàn chỉnh theo chuẩn công nghiệp.
*   Thực hiện quy trình ETL phức tạp xử lý đa nguồn dữ liệu bằng SSIS (đạt yêu cầu nâng cao).
*   Tạo báo cáo Power BI trực quan, chứng minh được giả thuyết về hiệu quả chính sách.

### 2. Hạn chế và Hướng phát triển
*   **Hạn chế:** Chưa tích hợp dữ liệu thời gian thực (Real-time streaming).
*   **Hướng phát triển:** Tích hợp API để lấy dữ liệu thời gian thực và áp dụng Machine Learning để dự báo ô nhiễm.

---

## TÀI LIỆU THAM KHẢO
1.  Kimball, R. (2013). *The Data Warehouse Toolkit*.
2.  Microsoft Documentation: SSIS, Power BI, SQL Server.
