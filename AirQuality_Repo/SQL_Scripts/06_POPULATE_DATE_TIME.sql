-- 1. Tạo dữ liệu cho bảng DimDate (Từ năm 2013 đến 2024)
DECLARE @StartDate DATE = '2013-01-01';
DECLARE @EndDate DATE = '2024-12-31';

WHILE @StartDate <= @EndDate
BEGIN
    INSERT INTO DimDate (DateKey, FullDate, DayOfWeek, Month, Quarter, Year)
    VALUES (
        CAST(CONVERT(VARCHAR(8), @StartDate, 112) AS INT), -- DateKey: 20130101
        @StartDate,
        DATEPART(dw, @StartDate),
        MONTH(@StartDate),
        DATEPART(qq, @StartDate),
        YEAR(@StartDate)
    );
    SET @StartDate = DATEADD(dd, 1, @StartDate);
END;

-- 2. Tạo dữ liệu cho bảng DimTime (24 giờ)
DECLARE @Hour INT = 0;
WHILE @Hour <= 23
BEGIN
    INSERT INTO DimTime (TimeKey, Time, Hour)
    VALUES (
        @Hour, -- TimeKey: 0, 1, 2... 23
        CAST(DATEADD(hour, @Hour, '00:00:00') AS TIME),
        @Hour
    );
    SET @Hour = @Hour + 1;
END;

-- Kiểm tra kết quả
SELECT COUNT(*) AS TotalDays FROM DimDate;
SELECT COUNT(*) AS TotalHours FROM DimTime;
