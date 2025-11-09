# Dữ liệu Nguồn: Giám sát Chất lượng Không khí Hà Nội

## 1. Giới thiệu

Tệp dữ liệu này là nguồn chính (Source Data) cho dự án Kho Dữ liệu (Data Warehouse) về Giám sát Chất lượng Không khí Đô thị. Dữ liệu được tổ chức dưới dạng bảng rộng (Wide Fact Table) với các chỉ số đo lường hàng giờ (Hourly Snapshot).

## 2. Nguồn Dữ liệu

| Mục | Chi tiết |
|---|---|
| **Tên Tệp** | `hanoi-aqi-weather-data.csv` |
| **Phạm vi** | Dữ liệu đo lường theo giờ tại Thành phố Hà Nội. |
| **Mục đích** | Cung cấp dữ liệu thô để xây dựng mô hình Star Schema và nạp (Load) vào bảng FactHourlyMeasurement. |

## 3. Cấu trúc Cột (Dùng cho ETL)

Quá trình ETL (Extract-Transform-Load) sử dụng các cột sau để xây dựng Star Schema:

### A. Cột Khóa & Bối cảnh (Dimensions)

| Tên Cột | Mô tả | Vai trò trong DW |
| :--- | :--- | :--- |
| **Local Time** | Thời điểm đo chính xác. | Nguồn để tách thành **LookupDate** và **LookupHour**. |
| **City** | Tên thành phố ("Hanoi"). | Khóa doanh nghiệp (Business Key) để tra cứu **LocationKey**. |

### B. Cột Số đo (Measures - Nạp vào FactHourlyMeasurement)

Đây là các chỉ số số hóa đã được chuyển đổi kiểu dữ liệu từ `string` sang `float` hoặc `int` trong quá trình ETL.

| Nhóm | Các Cột (Measures) | Kiểu dữ liệu Đích (SQL) |
| :--- | :--- | :--- |
| **Chất lượng Không khí** | AQI, PM25, CO, NO2, O3, PM10, SO2 | INT / FLOAT |
| **Thời tiết** | Temperature, Relative Humidity, Clouds, Wind Speed, Pressure, Precipitation, UV Index | FLOAT |

---

### 🏁 Hoàn tất:

1.  Dán nội dung trên vào cửa sổ Edit.
2.  Cuộn xuống dưới cùng (trên giao diện GitHub).
3.  Nhấn nút **"Commit changes..."** (Lưu thay đổi) để lưu tệp `README.md` của bạn.

Bạn đã hoàn thành việc mô tả thư mục `Data` của mình.
