-- =============================================================
-- MINH HỌA CÁC PHÉP TOÁN OLAP TRÊN KHO DỮ LIỆU (MỤC 6)
-- =============================================================
USE AirQuality_DW;
GO

-- 1. SLICE (Cắt lát)
-- Yêu cầu: Chỉ xem dữ liệu của ngày 2023-01-01
-- Giải thích: Cố định chiều Thời gian (Date) tại một giá trị cụ thể.
SELECT 
    D.FullDate,
    T.Time,
    F.AQI,
    F.Temperature
FROM FactHourlyMeasurement F
JOIN DimDate D ON F.DateKey = D.DateKey
JOIN DimTime T ON F.TimeKey = T.TimeKey
WHERE D.FullDate = '2023-01-01' -- Điều kiện Slice
ORDER BY T.TimeKey;
GO

-- 2. DICE (Cắt khối)
-- Yêu cầu: Xem dữ liệu AQI của Tháng 1 VÀ trong khung giờ cao điểm (07:00 - 09:00)
-- Giải thích: Cắt một khối dữ liệu con dựa trên điều kiện của 2 chiều (Date và Time).
SELECT 
    D.FullDate,
    T.Hour,
    F.AQI
FROM FactHourlyMeasurement F
JOIN DimDate D ON F.DateKey = D.DateKey
JOIN DimTime T ON F.TimeKey = T.TimeKey
WHERE D.Month = 1              -- Điều kiện chiều Date
  AND T.Hour BETWEEN 7 AND 9   -- Điều kiện chiều Time
ORDER BY D.FullDate, T.Hour;
GO

-- 3. ROLL-UP (Cuộn lên / Tổng hợp)
-- Yêu cầu: Tính AQI trung bình từ mức Giờ (Chi tiết) lên mức Tháng (Tổng hợp)
-- Giải thích: Loại bỏ chiều Time, gộp nhóm theo chiều Date (Month).
SELECT 
    D.Month,
    AVG(F.AQI) AS Avg_AQI,
    MAX(F.AQI) AS Max_AQI
FROM FactHourlyMeasurement F
JOIN DimDate D ON F.DateKey = D.DateKey
GROUP BY D.Month -- Roll-up theo Tháng
ORDER BY D.Month;
GO

-- 4. DRILL-DOWN (Khoan sâu) & ROLL-UP kết hợp (Sử dụng GROUP BY ROLLUP)
-- Yêu cầu: Xem báo cáo tổng hợp theo Năm -> Quý -> Tháng
-- Giải thích: Cung cấp cái nhìn từ tổng quan (Năm) xuống chi tiết (Tháng).
SELECT 
    D.Year,
    D.Quarter,
    D.Month,
    AVG(F.AQI) AS Avg_AQI,
    COUNT(*) AS Total_Measurements
FROM FactHourlyMeasurement F
JOIN DimDate D ON F.DateKey = D.DateKey
GROUP BY ROLLUP (D.Year, D.Quarter, D.Month);
-- Lưu ý kết quả:
-- Hàng có Month = NULL, Quarter = NULL là tổng của cả Năm.
-- Hàng có Month = NULL là tổng của Quý.
GO
