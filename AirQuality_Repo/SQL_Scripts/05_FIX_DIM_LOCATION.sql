-- =============================================================
-- KHẮC PHỤC LỖI THIẾT KẾ: LIÊN KẾT DIMLOCATION VÀ DIMCITY
-- Mục tiêu: Tạo mô hình Snowflake để hỗ trợ Filter đồng bộ trên Power BI
-- =============================================================
USE AirQuality_DW;
GO

-- BƯỚC 1: Thêm cột CityKey vào bảng DimLocation
-- Lưu ý: Để NULL trước vì chưa có dữ liệu, sau khi update xong mới set NOT NULL nếu muốn.
IF NOT EXISTS (SELECT * FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = 'DimLocation' AND COLUMN_NAME = 'CityKey')
BEGIN
    ALTER TABLE DimLocation
    ADD CityKey INT;
    PRINT 'Da them cot CityKey vao DimLocation';
END
GO

-- BƯỚC 2: Cập nhật dữ liệu CityKey dựa trên tên City có sẵn
-- Logic mapping: Tìm CityKey trong bảng DimCity có tên trùng với City trong DimLocation
UPDATE L
SET L.CityKey = C.CityKey
FROM DimLocation L
JOIN DimCity C ON L.City = C.CityName;
-- Xử lý trường hợp tên không khớp (Ví dụ Beijing vs Bắc Kinh), ta có thể update thủ công sau nếu cần
PRINT 'Da cap nhat du lieu CityKey';
GO

-- BƯỚC 3: Tạo Khóa ngoại (Foreign Key)
-- Ràng buộc: DimLocation.CityKey phải tham chiếu tới DimCity.CityKey
IF NOT EXISTS (SELECT * FROM sys.foreign_keys WHERE name = 'FK_DimLocation_DimCity')
BEGIN
    ALTER TABLE DimLocation
    ADD CONSTRAINT FK_DimLocation_DimCity
    FOREIGN KEY (CityKey) REFERENCES DimCity(CityKey);
    PRINT 'Da tao khoa ngoai FK_DimLocation_DimCity';
END
GO

-- KIỂM TRA LẠI KẾT QUẢ
SELECT TOP 5 LocationKey, City, CityKey FROM DimLocation;
