/****************************************************************/
/* DỰ ÁN: GIÁM SÁT CHẤT LƯỢNG KHÔNG KHÍ ĐÔ THỊ                 */
                       */
/****************************************************************/

USE AirQuality_DW;
GO

-- Nạp 'Hanoi' vào DimLocation
INSERT INTO DimLocation (City, CountryCode, Timezone)
VALUES ('Hanoi', 'VN', 'Asia/Ho_Chi_Minh');

-- Tự động nạp 3 năm dữ liệu (2022-2024) vào DimDate
DECLARE @StartDate DATE = '2022-01-01';
DECLARE @EndDate DATE = '2024-12-31';

WHILE @StartDate <= @EndDate
BEGIN
    INSERT INTO DimDate (DateKey, FullDate, DayOfWeek, Month, Quarter, Year)
    VALUES (
        CONVERT(INT, FORMAT(@StartDate, 'yyyyMMdd')),
        @StartDate,
        DATEPART(WEEKDAY, @StartDate),
        DATEPART(MONTH, @StartDate),
        DATEPART(QUARTER, @StartDate),
        DATEPART(YEAR, @StartDate)
    );
    SET @StartDate = DATEADD(DAY, 1, @StartDate);
END;

-- Tự động nạp 24 giờ vào DimTime
DECLARE @Hour INT = 0;
WHILE @Hour < 24
BEGIN
    INSERT INTO DimTime (TimeKey, Time, Hour)
    VALUES (
        @Hour * 100, -- Tạo Key dạng HH00 (vd: 0, 100, 200... 2300)
        TIMEFROMPARTS(@Hour, 0, 0, 0, 0), -- Tạo Time (vd: 00:00:00)
        @Hour
    );
    SET @Hour = @Hour + 1;
END;
GO