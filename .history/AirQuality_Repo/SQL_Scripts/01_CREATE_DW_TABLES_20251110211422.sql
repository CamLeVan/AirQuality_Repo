/****************************************************************/
/* DỰ ÁN: GIÁM SÁT CHẤT LƯỢNG KHÔNG KHÍ ĐÔ THỊ                 */
                        */
/****************************************************************/
USE master;
GO

-- Xóa DB cũ nếu tồn tại
IF EXISTS (SELECT * FROM sys.databases WHERE name = 'AirQuality_DW')
BEGIN
    ALTER DATABASE AirQuality_DW SET SINGLE_USER WITH ROLLBACK IMMEDIATE;
    DROP DATABASE AirQuality_DW;
END
GO

CREATE DATABASE AirQuality_DW;
GO
USE AirQuality_DW;
GO

-- Bảng Dim 1: Địa điểm (Location)
CREATE TABLE DimLocation (
    LocationKey INT PRIMARY KEY IDENTITY(1,1), -- Khóa nhân tạo
    City NVARCHAR(100) NOT NULL,
    CountryCode VARCHAR(10),
    Timezone VARCHAR(50)
);

-- Bảng Dim 2: Ngày (Date)
CREATE TABLE DimDate (
    DateKey INT PRIMARY KEY, -- Khóa tự nhiên (VD: 20230308)
    FullDate DATE NOT NULL,
    DayOfWeek INT,
    Month INT,
    Quarter INT,
    Year INT
);

-- Bảng Dim 3: Giờ (Time)
CREATE TABLE DimTime (
    TimeKey INT PRIMARY KEY, -- Khóa tự nhiên (VD: 0, 100, 200... 2300)
    Time TIME NOT NULL,
    Hour INT
);

-- Bảng Fact chính: Nơi chứa tất cả số đo
CREATE TABLE FactHourlyMeasurement (
    MeasurementKey BIGINT PRIMARY KEY IDENTITY(1,1),
    
    -- Khóa ngoại (Foreign Keys)
    LocationKey INT FOREIGN KEY REFERENCES DimLocation(LocationKey),
    DateKey INT FOREIGN KEY REFERENCES DimDate(DateKey),
    TimeKey INT FOREIGN KEY REFERENCES DimTime(TimeKey),
    
    -- Số đo Chất lượng không khí (Measures - AQI/Pollutants)
    AQI INT,
    CO FLOAT,
    NO2 FLOAT,
    O3 FLOAT,
    PM10 FLOAT,
    PM25 FLOAT,
    SO2 FLOAT,
    
    -- Số đo Thời tiết (Measures - Weather)
    Clouds FLOAT,
    Precipitation FLOAT,
    Pressure FLOAT,
    RelativeHumidity FLOAT,
    Temperature FLOAT,
    UVIndex FLOAT,
    WindSpeed FLOAT
);
GO