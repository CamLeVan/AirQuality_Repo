INSERT INTO DimLocation (City, CountryCode, Timezone)
VALUES 
('Hanoi', 'VN', 'Asia/Ho_Chi_Minh'),
('Beijing', 'CN', 'Asia/Shanghai');

-- Kiểm tra lại xem đã có dữ liệu chưa và ID là bao nhiêu
SELECT * FROM DimLocation;
