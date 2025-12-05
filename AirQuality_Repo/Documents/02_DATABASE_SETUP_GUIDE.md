# HƯỚNG DẪN CÀI ĐẶT CƠ SỞ DỮ LIỆU (DATABASE SETUP)

Tài liệu này hướng dẫn chi tiết các bước chuẩn bị môi trường và khởi tạo Database cho dự án Kho dữ liệu Chất lượng Không khí.

---

## 1. Yêu Cầu Hệ Thống (Prerequisites)

Trước khi bắt đầu, hãy đảm bảo máy tính của bạn đã cài đặt các phần mềm sau:

1.  **SQL Server 2019 (hoặc mới hơn):** Database Engine để lưu trữ kho dữ liệu.
2.  **SQL Server Management Studio (SSMS):** Công cụ quản lý và truy vấn SQL.
3.  **Visual Studio 2019/2022:**
    *   Cài đặt workload **"Data storage and processing"**.
    *   Cài đặt Extension **"SQL Server Integration Services Projects"**.
4.  **Power BI Desktop:** Công cụ làm báo cáo.

---

## 2. Khởi Tạo Database

### Bước 1: Tạo Database Trống
1.  Mở SSMS.
2.  Kết nối vào Server (`localhost` hoặc `.`).
3.  Mở cửa sổ New Query, chạy lệnh sau:
    ```sql
    CREATE DATABASE AirQuality_DW;
    GO
    ```

### Bước 2: Chạy Script Tạo Bảng (Schema)
1.  Mở file script: `SQL_Scripts/01_CREATE_DW_TABLES.sql`.
2.  Copy toàn bộ nội dung.
3.  Paste vào SSMS (đảm bảo đang chọn DB `AirQuality_DW`) và nhấn **Execute (F5)**.
4.  Tiếp tục chạy file script: `SQL_Scripts/04_UPDATE_SCHEMA_COMPLEX.sql` để cập nhật các bảng Fact nâng cao (`FactAnnualSummary`, `FactPolicyEvent`).

### Bước 3: Nạp Dữ Liệu Dimension (Dữ liệu tĩnh)
Các bảng Dimension (Chiều) cần có dữ liệu trước khi nạp bảng Fact.
1.  Chạy script: `SQL_Scripts/02_POPULATE_DIMS.sql` (Nạp DimLocation, DimPolicy).
2.  Chạy script: `SQL_Scripts/06_POPULATE_DATE_TIME.sql` (Nạp DimDate, DimTime).
    *   *Lưu ý:* Script này sẽ tự động sinh dữ liệu ngày tháng từ năm 2013 đến 2024.

---

## 3. Kiểm Tra Kết Quả

Sau khi chạy xong các script trên, hãy kiểm tra danh sách bảng trong Database:

```sql
USE AirQuality_DW;
GO

-- Kiểm tra danh sách bảng
SELECT TABLE_NAME 
FROM INFORMATION_SCHEMA.TABLES 
WHERE TABLE_TYPE = 'BASE TABLE';
```

**Kết quả mong đợi:** Bạn phải thấy các bảng sau:
*   `DimDate`
*   `DimTime`
*   `DimLocation` (hoặc `DimCity`)
*   `DimPolicy`
*   `FactHourlyMeasurement`
*   `FactAnnualSummary`
*   `FactPolicyEvent`

Nếu đầy đủ các bảng trên, bạn đã sẵn sàng chuyển sang bước ETL!
