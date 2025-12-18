# HƯỚNG DẪN CHI TIẾT TỪNG BƯỚC HOÀN THIỆN DỰ ÁN (STEP-BY-STEP WALKTHROUGH)

Tài liệu này là "Cẩm nang thực hành" chi tiết nhất. Chỉ cần làm theo đúng từng bước dưới đây, bạn chắc chắn sẽ hoàn thành dự án.

---

## GIAI ĐOẠN 1: XÂY DỰNG KHO DỮ LIỆU (SQL SERVER)
*Người thực hiện: Database Architect*

**Bước 1: Khởi tạo Database**
1.  Mở **SQL Server Management Studio (SSMS)** và kết nối vào máy chủ của bạn.
2.  Mở file script: `SQL_Scripts/01_CREATE_DW_TABLES.sql`.
3.  Nhấn **Execute (F5)**.
    *   *Kết quả:* Database `AirQuality_DW` xuất hiện trong cột bên trái (Object Explorer).

**Bước 2: Nâng cấp Schema (Quan trọng)**
1.  Mở tiếp file script: `SQL_Scripts/04_UPDATE_SCHEMA_COMPLEX.sql`.
2.  Nhấn **Execute (F5)**.
    *   *Kết quả:* Trong thư mục **Tables** của database, bạn sẽ thấy thêm các bảng mới: `DimCity`, `DimPolicy`, `FactPolicyEvent`, `FactAnnualSummary`.
    *   *Kiểm tra:* Chuột phải vào bảng `DimCity` -> Select Top 1000 Rows. Nếu thấy có dòng "Hanoi" và "Beijing" là thành công.

---


## GIAI ĐOẠN 2: CHUẨN BỊ DỮ LIỆU (DATA PREP)
*Người thực hiện: ETL Engineer*

**Bước 3: Kiểm tra file dữ liệu nguồn**
1.  Vào thư mục `Data/`.
2.  Đảm bảo có đủ 2 file:
    *   `hanoi-aqi-weather-data.csv` (Dữ liệu thật).
    *   `beijing_air_quality_2013_2023.csv` (Dữ liệu giả lập - Đã có sẵn).

---

## GIAI ĐOẠN 3: TÍCH HỢP DỮ LIỆU (ETL VỚI SSIS)
*Người thực hiện: ETL Engineer*
*Đây là phần khó nhất, hãy chú ý kỹ.*

**Bước 4: Tạo Project SSIS**
1.  Mở **Visual Studio**.
2.  Chọn **Create a new project** -> Tìm kiếm "Integration Services Project".
3.  Đặt tên project là `AirQuality_ETL`.

**Bước 5: Tạo Connection Managers (Quản lý kết nối)**
1.  Ở khung dưới cùng (Connection Managers), chuột phải -> **New OLE DB Connection**.
    *   Chọn Server Name của bạn -> Chọn Database `AirQuality_DW` -> OK.
2.  Chuột phải -> **New Flat File Connection**.
    *   Đặt tên: `Conn_HanoiCSV`.
    *   Browse chọn file `hanoi-aqi-weather-data.csv`.
    *   **Lưu ý:** Vào mục **Advanced**, kiểm tra cột `date` xem DataType có đúng là `date [DT_DATE]` hoặc chuỗi không.

**Bước 6: Xây dựng Data Flow cho Hà Nội**
1.  Kéo **Data Flow Task** vào màn hình Control Flow. Đổi tên thành "Import Hanoi Data".
2.  Double-click vào nó để vào tab Data Flow.
3.  **Source:** Kéo `Flat File Source` -> Chọn `Conn_HanoiCSV`.
4.  **Transformation 1 (Derived Column):**
    *   Kéo `Derived Column` vào, nối mũi tên xanh từ Source sang.
    *   Tạo cột mới tên `CityKey`.
    *   Expression: `1` (Vì trong SQL, Hanoi có ID là 1).
5.  **Transformation 2 (Data Conversion):**
    *   Kéo `Data Conversion` vào.
    *   Chọn các cột cần thiết (PM2.5, AQI...). Chuyển đổi kiểu dữ liệu cho khớp với SQL (Ví dụ: CSV là String thì chuyển sang DT_R8 cho số thực).
6.  **Destination:**
    *   Kéo `OLE DB Destination` -> Chọn bảng `FactHourlyMeasurement`.
    *   Vào **Mappings**: Nối các cột từ Input (cột đã Convert) sang Output (cột trong bảng SQL).

**Bước 7: Xây dựng Data Flow cho Bắc Kinh**
1.  Làm tương tự Bước 6, nhưng chọn file nguồn là Bắc Kinh.
2.  Trong `Derived Column`, set `CityKey` = `2` (Beijing).

**Bước 8: Chạy và Kiểm tra**
1.  Nhấn **Start** để chạy Package.
2.  Nếu thấy toàn màu xanh lá cây ✅ là OK.
3.  Vào SQL Server, chạy lệnh: `SELECT COUNT(*) FROM FactHourlyMeasurement`. Nếu ra số lớn (> 100.000 dòng) là thành công.

**Bước 9: Tổng hợp dữ liệu (Aggregation)**
*Bước này để tạo dữ liệu cho bảng tổng hợp năm, giúp Power BI chạy nhanh.*
1.  Vào SQL Server (SSMS).
2.  Chạy câu lệnh sau (Copy/Paste):
    ```sql
    INSERT INTO FactAnnualSummary (CityKey, Year, Avg_AQI, Avg_PM25, Avg_SO2)
    SELECT 
        CityKey,
        YEAR(DateKey) as Year, -- Lưu ý: Cần xử lý DateKey cho đúng format yyyyMMdd hoặc join DimDate
        AVG(AQI), AVG(PM25), AVG(SO2)
    FROM FactHourlyMeasurement
    GROUP BY CityKey, YEAR(DateKey);
    ```

---

## GIAI ĐOẠN 4: BÁO CÁO & TRỰC QUAN HÓA (POWER BI)
*Người thực hiện: BI Developer*

**Bước 10: Kết nối dữ liệu**
1.  Mở **Power BI Desktop**.
2.  **Get Data** -> **SQL Server**.
3.  Nhập Server Name -> Chọn Database `AirQuality_DW`.
4.  Chọn chế độ **Import**.
5.  Chọn các bảng: `FactHourlyMeasurement`, `FactAnnualSummary`, `DimCity`, `DimPolicy`, `FactPolicyEvent`. Nhấn **Load**.

**Bước 11: Xây dựng Data Model**
1.  Vào tab **Model View** (icon sơ đồ bên trái).
2.  Kéo thả để tạo liên kết (Relationship):
    *   `DimCity.CityKey` -> `FactHourlyMeasurement.CityKey`.
    *   `DimCity.CityKey` -> `FactAnnualSummary.CityKey`.
    *   `DimCity.CityKey` -> `FactPolicyEvent.CityKey`.
    *   (Tương tự với DimDate nếu có).

**Bước 12: Vẽ biểu đồ (Visualization)**
*   **Trang 1: So sánh Xu hướng (Trend Analysis)**
    *   Chọn biểu đồ **Line Chart**.
    *   Trục X: `Year` (từ bảng FactAnnualSummary).
    *   Trục Y: `Avg_PM25`.
    *   Legend (Chú giải): `CityName` (từ bảng DimCity).
    *   *Kết quả:* Bạn sẽ thấy 2 đường: Hà Nội (ngang hoặc tăng) và Bắc Kinh (giảm mạnh).

*   **Trang 2: Tác động Chính sách (Policy Impact)**
    *   Chọn biểu đồ **Combo Chart** (Line and Clustered Column).
    *   Cột (Column): `Avg_SO2` của Bắc Kinh.
    *   Trục X: `Year`.
    *   Thêm các đường tham chiếu (Constant Line) hoặc chú thích text tại các năm 2013, 2017 để ghi tên chính sách (Lấy từ `DimPolicy`).

**Bước 13: Xuất bản**
1.  Lưu file `.pbix`.
2.  Chụp ảnh màn hình các biểu đồ đẹp nhất để đưa vào Slide thuyết trình.

---
**Chúc các bạn thành công! Nếu gặp lỗi ở bước nào (đặc biệt là SSIS), hãy báo ngay để được hỗ trợ.**
