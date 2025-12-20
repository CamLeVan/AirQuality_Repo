# 🌍 Air Quality Dataset Documentation

## 1. Data Dictionary (Từ điển dữ liệu)
Bảng dữ liệu sau khi qua luồng xử lý ETL (Extract-Transform-Load) có cấu trúc chuẩn như sau:

| Column | Type | Description |
|--------|------|-------------|
| **City** | Str | Tên thành phố (Hanoi / Beijing) |
| **Date** | Date | Ngày quan trắc (Format: YYYY-MM-DD) |
| **Time** | Int | Giờ quan trắc (0-23) |
| **PM2.5** | Float | Nồng độ bụi mịn PM2.5 (µg/m³) |
| **AQI** | Int | Chỉ số chất lượng không khí (US EPA Standard) |
| **Temperature** | Float | Nhiệt độ môi trường (°C) |
| **Humidity** | Float | Độ ẩm tương đối (%) |
| **WindSpeed** | Float | Tốc độ gió (km/h) |
| **WeatherCondition**| Str | Trạng thái thời tiết (Clear, Cloudy, Rain...) |

---

## 2. Data Sources (Nguồn dữ liệu) & Methodology

Dự án sử dụng phương pháp **Hybrid Ingestion Approach** (Tiếp cận lai) để thu thập dữ liệu từ hai nguồn tin cậy nhất hiện nay.

### 🇨🇳 Beijing Data (2013 - 2023)
*   **Source:** **US Embassy Beijing Air Quality Monitor** & **UCI Machine Learning Repository**.
*   **Method:** Batch Processing (Xử lý theo lô).
*   **Process:**
    1.  Tải các `csv dump` lịch sử từ StateAir.net (Historical Data Archives).
    2.  Sử dụng Python (`pandas`) để làm sạch các giá trị Null (-999).
    3.  Hợp nhất (Merge) 11 file năm thành một Master Dataset.
*   **Reference:** [Beijing Multi-Site Air-Quality Data](https://archive.ics.uci.edu/ml/datasets/Beijing+PM2.5+Data)

### 🇻🇳 Hanoi Data (2013 - 2023)
*   **Source:** **OpenAQ Platform** (Aggregated from US Embassy Hanoi - Lang Ha Station & Vietnam CEM).
*   **Method:** API Real-time Fetching (Thu thập qua API).
*   **Process:**
    1.  Kết nối tới API Endpoint: `https://api.openaq.org/v2/measurements`.
    2.  Sử dụng script Python để phân trang (Pagination) và lấy dữ liệu lịch sử.
    3.  Áp dụng thuật toán **Linear Interpolation** để xử lý các khoảng trống dữ liệu (Missing Data) do lỗi cảm biến cục bộ.
*   **Reference:** [OpenAQ Hanoi Data Explorer](https://openaq.org/)

---

## 3. Tech Stack (Công nghệ làm sạch)
*   **Language:** Python 3.9
*   **Libraries:** Pandas, NumPy, Glob, OS, Requests.
*   **Pipeline Code:** `pipeline_data_ingestion.py` (Included in this folder).