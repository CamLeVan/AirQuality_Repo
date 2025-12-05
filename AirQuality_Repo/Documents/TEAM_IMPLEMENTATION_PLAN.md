# KẾ HOẠCH TRIỂN KHAI XÂY DỰNG SẢN PHẨM (TEAM WORK)
## MỤC TIÊU: HOÀN THIỆN SẢN PHẨM KHO DỮ LIỆU ĐỂ THI/BÁO CÁO

Để có sản phẩm hoàn chỉnh (Database + ETL + Dashboard) trong thời gian ngắn, nhóm 3 người cần chia việc song song theo quy trình **Data Engineering -> ETL -> BI**.

---

## 1. PHÂN CÔNG VAI TRÒ (ROLES)

### 👷 Thành viên 1: Database Engineer (Phụ trách SQL & Kho dữ liệu)
*   **Nhiệm vụ chính:** Xây dựng "khung xương" cho hệ thống. Đảm bảo Database chứa được dữ liệu phức tạp (Hà Nội & Bắc Kinh).
*   **Kỹ năng cần dùng:** SQL Server Management Studio (SSMS), T-SQL.

### 🚚 Thành viên 2: ETL Developer (Phụ trách Xử lý dữ liệu & SSIS)
*   **Nhiệm vụ chính:** "Vận chuyển" dữ liệu. Đưa dữ liệu từ file CSV (Python/Excel) vào trong SQL Server sạch sẽ, đúng định dạng.
*   **Kỹ năng cần dùng:** Visual Studio (SSIS), Python (chạy script sinh dữ liệu).

### 📊 Thành viên 3: BI Developer (Phụ trách Báo cáo & Power BI)
*   **Nhiệm vụ chính:** "Trang trí" và hiển thị. Biến dữ liệu thô trong SQL thành biểu đồ đẹp, có ý nghĩa để thuyết trình.
*   **Kỹ năng cần dùng:** Power BI Desktop, DAX.

---

## 2. CHECKLIST CÔNG VIỆC CỤ THỂ (TO-DO LIST)

### GIAI ĐOẠN 1: CHUẨN BỊ & KHỞI TẠO (Ngày 1)

#### 👷 Thành viên 1 (DB)
1.  [ ] **Cài đặt Database:** Mở SSMS, chạy script `SQL_Scripts/01_CREATE_DW_TABLES.sql` để tạo DB gốc.
2.  [ ] **Nâng cấp Schema:** Chạy tiếp script `SQL_Scripts/04_UPDATE_SCHEMA_COMPLEX.sql`.
    *   *Mục đích:* Tạo thêm bảng `DimCity`, `DimPolicy`, `FactAnnualSummary` để phục vụ bài toán so sánh nâng cao.
3.  [ ] **Kiểm tra:** Đảm bảo các bảng đã có đủ cột và Khóa ngoại (FK) được liên kết đúng (Vẽ Database Diagram trong SSMS để kiểm tra).

#### 🚚 Thành viên 2 (ETL)
1.  [ ] **Chuẩn bị Dữ liệu:**
    *   Chạy file `Data/generate_beijing_data.py` để sinh ra file `beijing_air_quality_2013_2023.csv`.
    *   Kiểm tra file `hanoi-aqi-weather-data.csv` xem có bị lỗi font hay định dạng ngày tháng không.
2.  [ ] **Tạo Project SSIS:** Tạo mới một Integration Services Project trong Visual Studio.

#### 📊 Thành viên 3 (BI)
1.  [ ] **Lên Layout Dashboard:** Vẽ nháp ra giấy bố cục 3 trang báo cáo:
    *   Trang 1: Tổng quan Hà Nội (Đồng hồ đo AQI, Biểu đồ nhiệt).
    *   Trang 2: So sánh Hà Nội vs Bắc Kinh (Biểu đồ đường chạy dài 10 năm).
    *   Trang 3: Phân tích Chính sách (Biểu đồ kết hợp Cột & Đường).

---

### GIAI ĐOẠN 2: THỰC HIỆN KỸ THUẬT (Ngày 2-3)

#### 👷 Thành viên 1 (DB)
1.  [ ] **Viết Stored Procedure tổng hợp:**
    *   Viết câu lệnh SQL để tự động tính toán từ bảng `FactHourlyMeasurement` (chi tiết) -> đổ vào bảng `FactAnnualSummary` (tổng hợp năm).
    *   *Gợi ý:* `INSERT INTO FactAnnualSummary SELECT CityKey, YEAR(Date), AVG(PM25)... FROM ... GROUP BY ...`
2.  [ ] **Hỗ trợ ETL:** Kiểm tra xem dữ liệu đổ vào có bị lỗi khóa ngoại không.

#### 🚚 Thành viên 2 (ETL)
1.  [ ] **Xây dựng Data Flow (Hà Nội):**
    *   Dùng `Flat File Source` đọc file Hà Nội -> `Data Conversion` (ép kiểu) -> `OLE DB Destination` (bảng FactHourly).
2.  [ ] **Xây dựng Data Flow (Bắc Kinh):**
    *   Tương tự Hà Nội, nhưng cần map thêm cột `CityKey` (Set cứng giá trị cho Bắc Kinh).
3.  [ ] **Nạp Dimensions:**
    *   Tạo luồng nạp dữ liệu cho `DimCity` (Hanoi, Beijing) và `DimPolicy` (Copy từ file Excel hoặc Insert cứng bằng SQL).

#### 📊 Thành viên 3 (BI)
1.  [ ] **Kết nối dữ liệu:** Mở Power BI -> Get Data -> SQL Server -> Chọn Database `AirQuality_DW`.
2.  [ ] **Xây dựng Model:** Vào tab Model view, nối các bảng Dim với Fact (theo sơ đồ sao).
3.  [ ] **Tạo Measures (DAX):**
    *   Viết các hàm tính toán: `Avg AQI = AVERAGE(FactHourly[AQI])`, `Số ngày ô nhiễm = CALCULATE(COUNTROWS(...), Filter(AQI > 150))`.

---

### GIAI ĐOẠN 3: HOÀN THIỆN & TÍCH HỢP (Ngày 4)

#### 👷 Thành viên 1 (DB)
1.  [ ] **Tối ưu:** Tạo Index cho các cột hay dùng để query (DateKey, CityKey) giúp Power BI chạy nhanh hơn.
2.  [ ] **Backup:** Backup file `.bak` của Database để nộp bài.

#### 🚚 Thành viên 2 (ETL)
1.  [ ] **Chạy toàn bộ quy trình:** Chạy full package SSIS xem có lỗi đỏ không.
2.  [ ] **Kiểm tra dữ liệu:** Select thử trong SQL xem bảng `FactHourlyMeasurement` đã có đủ dữ liệu cả 2 thành phố chưa.

#### 📊 Thành viên 3 (BI)
1.  [ ] **Vẽ biểu đồ:** Hoàn thiện 3 trang báo cáo theo layout đã thiết kế.
2.  [ ] **Kể chuyện:** Thêm các Textbox chú thích vào biểu đồ (Ví dụ: Mũi tên chỉ vào năm 2017 ghi "Cấm than đá").
3.  [ ] **Xuất file:** Lưu file `.pbix` hoàn chỉnh.

---

## 3. CÁCH PHỐI HỢP (WORKFLOW)
*   **Bước 1:** Ông **DB** phải tạo xong bảng thì ông **ETL** mới có chỗ để đổ dữ liệu vào. -> **DB làm trước.**
*   **Bước 2:** Ông **ETL** phải đổ xong dữ liệu thì ông **BI** mới có cái để vẽ. -> **ETL làm giữa.**
*   **Bước 3:** Tuy nhiên, ông **BI** có thể vẽ layout trước bằng dữ liệu giả (Excel) trong lúc chờ 2 ông kia, sau đó chỉ cần đổi nguồn dữ liệu (Change Data Source) sang SQL là xong.

---
**Lưu ý:** Để kịp tiến độ, tôi (AI) có thể hỗ trợ các bạn làm ngay phần việc của **Thành viên 1 (DB)** và **Thành viên 2 (ETL - phần Python)**. Các bạn chỉ cần tập trung vào SSIS và Power BI.
