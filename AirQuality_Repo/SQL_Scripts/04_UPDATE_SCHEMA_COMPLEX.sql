-- =============================================================
-- NÂNG CẤP SCHEMA: HỖ TRỢ PHÂN TÍCH SO SÁNH & CHÍNH SÁCH
-- =============================================================
USE AirQuality_DW;
GO

-- 1. Bảng DimCity (Mới - Chuẩn hóa địa lý)
-- Lý do: Tách biệt Thành phố để dễ dàng so sánh giữa các thành phố lớn (Hanoi vs Beijing)
CREATE TABLE DimCity (
    CityKey INT PRIMARY KEY IDENTITY(1,1),
    CityName NVARCHAR(100),
    CountryName NVARCHAR(100),
    Population INT, -- Dân số (Yếu tố ảnh hưởng ô nhiễm)
    Area FLOAT      -- Diện tích
);
GO

-- 2. Bảng DimPolicy (Mới - Trái tim của phân tích nguyên nhân)
-- Lý do: Lưu trữ các giải pháp/chính sách đã áp dụng để giảm ô nhiễm
CREATE TABLE DimPolicy (
    PolicyKey INT PRIMARY KEY IDENTITY(1,1),
    PolicyName NVARCHAR(200),
    PolicyType NVARCHAR(50), -- VD: Giao thông, Công nghiệp, Năng lượng
    Description NVARCHAR(500)
);
GO

-- 3. Bảng FactPolicyEvent (Mới - Sự kiện áp dụng chính sách)
-- Lý do: Biết được KHI NÀO chính sách bắt đầu để so sánh Before/After
CREATE TABLE FactPolicyEvent (
    EventKey INT PRIMARY KEY IDENTITY(1,1),
    CityKey INT FOREIGN KEY REFERENCES DimCity(CityKey),
    DateKey INT FOREIGN KEY REFERENCES DimDate(DateKey),
    PolicyKey INT FOREIGN KEY REFERENCES DimPolicy(PolicyKey),
    ImpactLevel NVARCHAR(50) -- Dự kiến tác động: Cao/Trung bình/Thấp
);
GO

-- 4. Bảng FactAnnualSummary (Mới - Aggregate Table)
-- Lý do: Bảng tổng hợp theo năm để truy vấn nhanh xu hướng dài hạn (10 năm)
-- Thay vì query hàng triệu dòng ở FactHourly, ta query bảng này cực nhanh.
CREATE TABLE FactAnnualSummary (
    SummaryKey INT PRIMARY KEY IDENTITY(1,1),
    CityKey INT FOREIGN KEY REFERENCES DimCity(CityKey),
    Year INT,
    Avg_AQI FLOAT,
    Avg_PM25 FLOAT,
    Avg_SO2 FLOAT,
    Max_AQI INT,
    Good_Days INT, -- Số ngày không khí tốt
    Polluted_Days INT -- Số ngày ô nhiễm
);
GO

-- 5. Nạp dữ liệu mẫu cho DimPolicy (Dữ liệu thực tế từ Bắc Kinh & Đề xuất cho Hà Nội)
INSERT INTO DimPolicy (PolicyName, PolicyType, Description)
VALUES 
(N'Clean Air Action Plan (2013-2017)', N'Tổng hợp', N'Kế hoạch hành động không khí sạch: Giảm than, kiểm soát xe cộ.'),
(N'Coal-to-Gas/Electricity', N'Năng lượng', N'Chuyển đổi lò sưởi/nhà máy nhiệt điện than sang dùng khí gas hoặc điện.'),
(N'National VI Emission Standard', N'Giao thông', N'Tiêu chuẩn khí thải xe cơ giới nghiêm ngặt nhất (tương đương Euro 6).'),
(N'Red Alert System', N'Cảnh báo', N'Hệ thống cảnh báo đỏ: Đóng cửa trường học, hạn chế xe khi ô nhiễm cực đoan.'),
(N'Relocation of Polluting Industries', N'Công nghiệp', N'Di dời các nhà máy thép, xi măng ra khỏi nội đô.');
GO

-- 6. Nạp dữ liệu mẫu cho DimCity
INSERT INTO DimCity (CityName, CountryName, Population)
VALUES 
('Hanoi', 'Vietnam', 8500000),
('Beijing', 'China', 21500000);
GO
