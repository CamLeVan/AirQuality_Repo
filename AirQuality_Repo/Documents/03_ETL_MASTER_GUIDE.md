# HƯỚNG DẪN TRIỂN KHAI ETL TOÀN TẬP VỚI SSIS (MASTER GUIDE)

Tài liệu này là hướng dẫn kỹ thuật duy nhất bạn cần để xây dựng toàn bộ quy trình ETL cho dự án, bao gồm cả 3 bảng Fact: Hourly, Annual, và Policy.

---

## PHẦN 1: KHỞI TẠO PROJECT
1.  Mở **Visual Studio**.
2.  Tạo mới project **Integration Services Project**.
3.  Đặt tên: `AirQuality_ETL`.
4.  Trong vùng **Connection Managers**, tạo kết nối tới SQL Server (`localhost.AirQuality_DW`) và đặt tên là `Conn_SQL_DW`.

---

## PHẦN 2: NẠP DỮ LIỆU CHI TIẾT (FACT HOURLY MEASUREMENT)
*Mục tiêu: Nạp dữ liệu từ file CSV vào bảng Fact chính.*

### 1. Chuẩn bị Connection Manager
*   Tạo **Flat File Connection Manager** cho file `hanoi-aqi-weather-data.csv`.
*   **Quan trọng:** Vào tab **Advanced**, đổi kiểu dữ liệu của các cột số (`AQI`, `PM2.5`...) thành **float [DT_R4]** và cột thời gian thành **database timestamp**.

### 2. Thiết kế Data Flow (`DFT_Load_AirQuality`)
1.  **Flat File Source:** Đọc file CSV.
2.  **Derived Column:** Tạo các cột khóa:
    *   `DateKey`: `(DT_I4)(YEAR([Local Time]) * 10000 + MONTH([Local Time]) * 100 + DAY([Local Time]))`
    *   `TimeKey`: `(DT_I4)DATEPART("hh", [Local Time])`
    *   `LocationKey`: `1` (cho Hà Nội) hoặc `2` (cho Bắc Kinh).
3.  **Data Conversion:** Ép kiểu lại các cột số liệu sang `DT_R4` (nếu cần thiết).
4.  **OLE DB Destination:** Nạp vào bảng `FactHourlyMeasurement`. Map các cột tương ứng.

---

## PHẦN 3: TÍNH TOÁN TỔNG HỢP (FACT ANNUAL SUMMARY)
*Mục tiêu: Tự động tính trung bình năm từ dữ liệu chi tiết.*

### Thiết kế Data Flow (`DFT_Load_AnnualSummary`)
1.  **OLE DB Source:**
    *   Dùng SQL Command để lấy dữ liệu từ `FactHourlyMeasurement` và `DimDate`.
    *   Query: `SELECT LocationKey, Year, AQI, PM25... FROM FactHourly... JOIN DimDate...`
2.  **Sort:** Sắp xếp theo `LocationKey` và `Year`.
3.  **Aggregate:**
    *   Group by: `LocationKey`, `Year`.
    *   Average: `AQI`, `PM25`, `SO2`.
    *   Maximum: `AQI`.
4.  **Data Conversion:** Ép kiểu các cột Average sang `DT_R8` (Double).
5.  **OLE DB Destination:** Nạp vào bảng `FactAnnualSummary`.

---

## PHẦN 4: XỬ LÝ SỰ KIỆN CHÍNH SÁCH (FACT POLICY EVENT)
*Mục tiêu: Nạp dữ liệu sự kiện và tra cứu ID (Lookup) từ các bảng Dimension.*

### Thiết kế Data Flow (`DFT_Load_PolicyEvents`)
1.  **Flat File Source:** Đọc file `policy_events.csv`.
2.  **Data Conversion (Quan trọng):**
    *   Chuyển `CityName` và `PolicyName` sang **Unicode string [DT_WSTR]**.
3.  **Lookup City:**
    *   Kết nối bảng `DimCity`.
    *   Nối `CityName_WSTR` -> `CityName`.
    *   Output: `CityKey`.
4.  **Lookup Policy:**
    *   Kết nối bảng `DimPolicy`.
    *   Nối `PolicyName_WSTR` -> `PolicyName`.
    *   Output: `PolicyKey`.
5.  **Derived Column:**
    *   Tạo `DateKey` từ cột ngày tháng gốc: `(DT_I4)(YEAR([EventDate])*10000 + ...)`
6.  **OLE DB Destination:**
    *   Nạp vào bảng `FactPolicyEvent`.
    *   Map: `CityKey`, `PolicyKey`, `DateKey`, `ImpactLevel`.

---

## PHẦN 5: CHẠY VÀ KIỂM TRA
1.  Trong Control Flow, nối các Task theo thứ tự: `Hourly` -> `Annual` -> `Policy`.
2.  Nhấn **Start**.
3.  Kiểm tra toàn bộ các luồng chuyển xanh.
4.  Vào SQL Server kiểm tra số lượng dòng trong 3 bảng Fact.
